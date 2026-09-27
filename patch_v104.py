from pathlib import Path

# Version
p=Path("build.gradle")
s=p.read_text().replace("version = '1.0.3'","version = '1.0.4'").replace("version = '1.0.2'","version = '1.0.4'")
p.write_text(s)

# Exact timing: roulette sound is ~14.814 s = 296 ticks at 20 TPS.
Path("src/main/java/com/challengecore/client/ClientState.java").write_text(r'''package com.challengecore.client;

public final class ClientState {
    public static final int DEATH_TOTAL=160;
    public static final int ROULETTE_TOTAL=296;
    public static int deathTicks=0,rouletteTicks=0,rouletteOutcome=0,swordTicks=0;
    public static String deadName="";
    public static void startDeath(String name){deadName=name;deathTicks=DEATH_TOTAL;}
    public static void startRoulette(int outcome){rouletteOutcome=Math.floorMod(outcome,8);rouletteTicks=ROULETTE_TOTAL;}
    public static void startSword(int ticks){swordTicks=ticks;}
    public static void tick(){
        if(deathTicks>0)deathTicks--;
        if(rouletteTicks>0)rouletteTicks--;
        if(swordTicks>0)swordTicks--;
    }
    private ClientState(){}
}
''')

Path("src/main/java/com/challengecore/client/ClientEvents.java").write_text(r'''package com.challengecore.client;

import com.challengecore.ChallengeCore;
import com.challengecore.client.audio.BossAudioController;
import com.challengecore.client.render.ChallengeBossRenderer;
import com.challengecore.client.render.GrillRenderer;
import com.challengecore.client.render.SlotMachineRenderer;
import com.challengecore.client.screen.AtmScreen;
import com.challengecore.client.screen.SlotConfigScreen;
import com.challengecore.registry.ModBlockEntities;
import com.challengecore.registry.ModEntities;
import com.challengecore.registry.ModMenus;
import com.challengecore.registry.ModSounds;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.MenuScreens;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.client.event.RenderGuiOverlayEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;

@Mod.EventBusSubscriber(modid=ChallengeCore.MODID,value=Dist.CLIENT,bus=Mod.EventBusSubscriber.Bus.MOD)
public final class ClientEvents {
    private static final ResourceLocation DEATH_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/death_overlay.png");
    private static final ResourceLocation SWORD_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/blood_attack.png");
    private static final ResourceLocation[] ROULETTE_ATLAS=new ResourceLocation[8];
    static{
        for(int i=0;i<8;i++)ROULETTE_ATLAS[i]=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette_"+i+".png");
    }

    @SubscribeEvent public static void clientSetup(FMLClientSetupEvent e){
        e.enqueueWork(()->{
            MenuScreens.register(ModMenus.ATM.get(),AtmScreen::new);
            MenuScreens.register(ModMenus.SLOT_CONFIG.get(),SlotConfigScreen::new);
        });
    }
    @SubscribeEvent public static void registerRenderers(EntityRenderersEvent.RegisterRenderers e){
        e.registerEntityRenderer(ModEntities.BOSS.get(),ChallengeBossRenderer::new);
        e.registerBlockEntityRenderer(ModBlockEntities.SLOT_MACHINE.get(),SlotMachineRenderer::new);
        e.registerBlockEntityRenderer(ModBlockEntities.GRILL.get(),GrillRenderer::new);
    }
    @SubscribeEvent public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions e){
        e.registerLayerDefinition(ChallengeBossRenderer.LAYER,com.challengecore.client.render.ChallengeBossModel::createBodyLayer);
    }

    @Mod.EventBusSubscriber(modid=ChallengeCore.MODID,value=Dist.CLIENT,bus=Mod.EventBusSubscriber.Bus.FORGE)
    public static class ForgeClient{
        private static int lastDeath=0,lastRoulette=0;

        @SubscribeEvent public static void tick(TickEvent.ClientTickEvent e){
            if(e.phase==TickEvent.Phase.END){ClientState.tick();BossAudioController.tick();}
        }

        @SubscribeEvent public static void overlay(RenderGuiOverlayEvent.Post e){
            GuiGraphics g=e.getGuiGraphics();
            int w=g.guiWidth(),h=g.guiHeight();

            if(ClientState.deathTicks>0){
                if(lastDeath==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.DEATH.get(),1f));
                float elapsed=ClientState.DEATH_TOTAL-ClientState.deathTicks;
                float scale;
                if(elapsed<18f){
                    float t=elapsed/18f;
                    scale=.04f+1.12f*(1f-(float)Math.pow(1f-t,3));
                }else if(elapsed<32f){
                    float t=(elapsed-18f)/14f;
                    scale=1.16f-.16f*t;
                }else if(ClientState.deathTicks<32){
                    float t=ClientState.deathTicks/32f;
                    scale=.05f+.95f*t;
                }else scale=1f;

                float alpha=ClientState.deathTicks<22?Math.max(0f,ClientState.deathTicks/22f):1f;
                int size=(int)(Math.min(w,h)*.52f);
                RenderSystem.enableBlend();
                RenderSystem.setShaderColor(1f,1f,1f,alpha);
                g.pose().pushPose();
                g.pose().translate(w/2f,h/2f-22,0);
                g.pose().scale(scale,scale,1f);
                g.blit(DEATH_TEX,-size/2,-size/2,0,0,size,size,512,512);
                g.pose().popPose();
                RenderSystem.setShaderColor(1f,1f,1f,1f);
                RenderSystem.disableBlend();
                g.drawCenteredString(Minecraft.getInstance().font,ClientState.deadName+" ha muerto",w/2,h/2+size/2-2,0xFFFF3030);
            }
            lastDeath=ClientState.deathTicks;

            if(ClientState.rouletteTicks>0){
                if(lastRoulette==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.ROULETTE_SPIN.get(),1f));

                int elapsed=ClientState.ROULETTE_TOTAL-ClientState.rouletteTicks;
                // Reference pack has 142 animation frames. Spread those 142 frames over the
                // 296 tick audio so image and sound ALWAYS end together.
                int frame=Math.min(141,(elapsed*142)/ClientState.ROULETTE_TOTAL);
                int col=frame%8,row=frame/8;
                int u=col*256,v=row*256;
                int size=(int)(Math.min(w,h)*.62f);

                float appear=Math.min(1f,elapsed/10f);
                float disappear=Math.min(1f,ClientState.rouletteTicks/12f);
                float s=Math.min(appear,disappear);
                int draw=Math.max(1,(int)(size*s));
                int x=w/2-draw/2,y=h/2-draw/2;

                RenderSystem.enableBlend();
                g.blit(ROULETTE_ATLAS[Math.floorMod(ClientState.rouletteOutcome,8)],x,y,draw,draw,u,v,256,256,2048,4608);
                RenderSystem.disableBlend();

                if(frame>=112){
                    String[] names={"VERDE","AMARILLO","NARANJA","ROJO","ROSA","MORADO","AZUL","CIAN"};
                    int[] colors={0xFF11D33F,0xFFFFD51F,0xFFFF9513,0xFFFF444A,0xFFFF45C1,0xFF9148E7,0xFF3859E9,0xFF27C4D5};
                    int o=Math.floorMod(ClientState.rouletteOutcome,8);
                    g.drawCenteredString(Minecraft.getInstance().font,names[o],w/2,h/2+size/2+8,colors[o]);
                }
            }
            lastRoulette=ClientState.rouletteTicks;

            if(ClientState.swordTicks>0){
                RenderSystem.enableBlend();
                g.blit(SWORD_TEX,0,0,0,0,w,h,512,512);
                RenderSystem.disableBlend();
            }
        }
    }
    private ClientEvents(){}
}
''')

# More articulated / layered samurai model and stronger idle/special motion.
Path("src/main/java/com/challengecore/client/render/ChallengeBossModel.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.entity.ChallengeBossEntity;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;

public class ChallengeBossModel extends HierarchicalModel<ChallengeBossEntity>{
    private final ModelPart root,torso,head,leftArm,rightArm,leftLeg,rightLeg,sword,backSword,mantle,skirt;

    public ChallengeBossModel(ModelPart root){
        this.root=root;torso=root.getChild("torso");head=root.getChild("head");
        leftArm=root.getChild("left_arm");rightArm=root.getChild("right_arm");
        leftLeg=root.getChild("left_leg");rightLeg=root.getChild("right_leg");
        sword=rightArm.getChild("sword");backSword=root.getChild("back_sword");
        mantle=root.getChild("mantle");skirt=root.getChild("skirt");
    }

    public static LayerDefinition createBodyLayer(){
        MeshDefinition mesh=new MeshDefinition();PartDefinition r=mesh.getRoot();

        PartDefinition torso=r.addOrReplaceChild("torso",
            CubeListBuilder.create()
                .texOffs(0,32).addBox(-7,-10,-4,14,18,8,new CubeDeformation(.35f))
                .texOffs(48,32).addBox(-8,-8,-5,16,5,10,new CubeDeformation(.35f))
                .texOffs(0,54).addBox(-6,-2,-5,12,11,10,new CubeDeformation(.18f)),
            PartPose.offset(0,5,0));
        torso.addOrReplaceChild("chest_plate",
            CubeListBuilder.create().texOffs(48,50).addBox(-5,-8,-1,10,12,2,new CubeDeformation(.28f)),
            PartPose.offset(0,0,-4.35f));
        torso.addOrReplaceChild("belt",
            CubeListBuilder.create().texOffs(0,76).addBox(-7,-1,-4,14,4,8,new CubeDeformation(.22f)),
            PartPose.offset(0,7,0));

        PartDefinition head=r.addOrReplaceChild("head",
            CubeListBuilder.create()
                .texOffs(0,0).addBox(-5,-6,-5,10,10,10,new CubeDeformation(.12f))
                .texOffs(40,0).addBox(-6,-8,-6,12,5,12,new CubeDeformation(.28f))
                .texOffs(40,20).addBox(-6,-3,-6.5f,12,4,2,new CubeDeformation(.08f)),
            PartPose.offset(0,-9,0));
        head.addOrReplaceChild("mask",
            CubeListBuilder.create().texOffs(72,20).addBox(-4,-1,-1,8,5,2,new CubeDeformation(.12f)),
            PartPose.offset(0,-1,-5.8f));
        head.addOrReplaceChild("brow",
            CubeListBuilder.create().texOffs(92,20).addBox(-5,-1,-1,10,2,2,new CubeDeformation(.1f)),
            PartPose.offset(0,-3,-6f));
        head.addOrReplaceChild("crest",
            CubeListBuilder.create().texOffs(82,0).addBox(-1,-13,-1,2,13,2,new CubeDeformation(.1f)),
            PartPose.offset(0,-5,0));
        head.addOrReplaceChild("crest_tip",
            CubeListBuilder.create().texOffs(90,0).addBox(-1,-8,-1,2,9,2),
            PartPose.offsetAndRotation(0,-17,0,0,0,.62f));
        head.addOrReplaceChild("horn_l",
            CubeListBuilder.create().texOffs(100,0).addBox(0,-1,-1,9,2,2),
            PartPose.offsetAndRotation(4,-8,0,0,0,-.68f));
        head.addOrReplaceChild("horn_r",
            CubeListBuilder.create().texOffs(100,0).mirror().addBox(-9,-1,-1,9,2,2),
            PartPose.offsetAndRotation(-4,-8,0,0,0,.68f));

        PartDefinition la=r.addOrReplaceChild("left_arm",
            CubeListBuilder.create()
                .texOffs(0,92).addBox(0,-3,-3,5,19,6,new CubeDeformation(.18f))
                .texOffs(24,92).addBox(-1,-6,-6,9,7,12,new CubeDeformation(.34f))
                .texOffs(60,92).addBox(0,7,-4,6,8,8,new CubeDeformation(.22f)),
            PartPose.offset(7,-2,0));
        la.addOrReplaceChild("shoulder_spike",
            CubeListBuilder.create().texOffs(88,88).addBox(0,-2,-2,9,3,4),
            PartPose.offsetAndRotation(4,-5,0,0,0,-.5f));

        PartDefinition ra=r.addOrReplaceChild("right_arm",
            CubeListBuilder.create()
                .texOffs(0,92).mirror().addBox(-5,-3,-3,5,19,6,new CubeDeformation(.18f))
                .texOffs(24,92).mirror().addBox(-8,-6,-6,9,7,12,new CubeDeformation(.34f))
                .texOffs(60,92).mirror().addBox(-6,7,-4,6,8,8,new CubeDeformation(.22f)),
            PartPose.offset(-7,-2,0));
        ra.addOrReplaceChild("shoulder_spike",
            CubeListBuilder.create().texOffs(88,88).mirror().addBox(-9,-2,-2,9,3,4),
            PartPose.offsetAndRotation(-4,-5,0,0,0,.5f));

        ra.addOrReplaceChild("sword",
            CubeListBuilder.create()
                .texOffs(76,52).addBox(-1,-4,-1,2,28,2)
                .texOffs(88,52).addBox(-2,21,-2,4,12,4)
                .texOffs(104,52).addBox(-7,19,-1,14,2,2),
            PartPose.offsetAndRotation(-2,9,-1,-.18f,0,0));

        r.addOrReplaceChild("back_sword",
            CubeListBuilder.create()
                .texOffs(76,52).addBox(-1,-5,-1,2,32,2)
                .texOffs(88,52).addBox(-2,24,-2,4,13,4)
                .texOffs(104,52).addBox(-7,22,-1,14,2,2),
            PartPose.offsetAndRotation(5,-11,4,-.58f,0,-.76f));

        PartDefinition mantle=r.addOrReplaceChild("mantle",
            CubeListBuilder.create().texOffs(64,108).addBox(-10,-2,-2,20,5,4,new CubeDeformation(.22f)),
            PartPose.offset(0,-3,4));
        for(int i=0;i<7;i++){
            mantle.addOrReplaceChild("feather"+i,
                CubeListBuilder.create().texOffs(96,108).addBox(-1,-1,0,2,12,2),
                PartPose.offsetAndRotation(-9+i*3,-1,1,.5f,0,(i-3)*.13f));
        }

        PartDefinition skirt=r.addOrReplaceChild("skirt",
            CubeListBuilder.create().texOffs(0,112).addBox(-7,-1,-5,14,8,10,new CubeDeformation(.14f)),
            PartPose.offset(0,12,0));
        skirt.addOrReplaceChild("front_plate",
            CubeListBuilder.create().texOffs(48,112).addBox(-4,0,-1,8,9,2,new CubeDeformation(.1f)),
            PartPose.offset(0,1,-5.1f));
        skirt.addOrReplaceChild("left_plate",
            CubeListBuilder.create().texOffs(70,112).addBox(0,0,-4,2,9,8,new CubeDeformation(.1f)),
            PartPose.offset(6.8f,1,0));
        skirt.addOrReplaceChild("right_plate",
            CubeListBuilder.create().texOffs(70,112).mirror().addBox(-2,0,-4,2,9,8,new CubeDeformation(.1f)),
            PartPose.offset(-6.8f,1,0));

        r.addOrReplaceChild("left_leg",
            CubeListBuilder.create().texOffs(52,76).addBox(-2,-1,-2,5,17,5,new CubeDeformation(.12f)),
            PartPose.offset(3,16,0));
        r.addOrReplaceChild("right_leg",
            CubeListBuilder.create().texOffs(52,76).mirror().addBox(-3,-1,-2,5,17,5,new CubeDeformation(.12f)),
            PartPose.offset(-3,16,0));

        return LayerDefinition.create(mesh,128,128);
    }

    @Override public ModelPart root(){return root;}

    @Override public void setupAnim(ChallengeBossEntity e,float limbSwing,float limbAmount,float age,float yaw,float pitch){
        float idle=(float)Math.sin(age*.085f);
        float breathe=(float)Math.sin(age*.12f);

        head.yRot=yaw*((float)Math.PI/180f);
        head.xRot=pitch*((float)Math.PI/180f)+idle*.025f;
        torso.xScale=1f+breathe*.012f;torso.yScale=1f+breathe*.018f;torso.zScale=1f+breathe*.012f;
        mantle.xRot=.04f+idle*.035f;
        skirt.xRot=idle*.012f;

        rightArm.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.05f*limbAmount + idle*.035f;
        leftArm.xRot=(float)Math.cos(limbSwing*.6662)*1.05f*limbAmount - idle*.035f;
        rightLeg.xRot=(float)Math.cos(limbSwing*.6662)*1.15f*limbAmount;
        leftLeg.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.15f*limbAmount;
        rightArm.yRot=rightArm.zRot=leftArm.yRot=leftArm.zRot=0;
        sword.visible=false;backSword.visible=true;

        int state=e.getAttackState();
        if(state==1){
            float pulse=(float)Math.sin(age*.75f)*.12f;
            rightArm.xRot=-1.58f+pulse;leftArm.xRot=-1.58f-pulse;
            rightArm.yRot=-.3f;leftArm.yRot=.3f;
            torso.xRot=-.08f;
        }else if(state==2){
            rightArm.xRot=-2.25f;leftArm.xRot=-2.25f;
            rightArm.zRot=-.5f;leftArm.zRot=.5f;
            torso.xRot=.08f+(float)Math.sin(age*.35f)*.035f;
        }else if(state==3){
            sword.visible=true;backSword.visible=false;
            float stab=(float)Math.sin(age*.9f);
            rightArm.xRot=-1.8f+stab*.62f;rightArm.yRot=-.28f;
            leftArm.xRot=-.45f;leftArm.yRot=.18f;
            torso.yRot=stab*.1f;
        }else{
            torso.xRot=0;torso.yRot=0;
        }

        for(int i=0;i<7;i++){
            ModelPart f=mantle.getChild("feather"+i);
            f.xRot=.5f+(float)Math.sin(age*.12f+i*.45f)*.06f;
        }
    }
}
''')
