from pathlib import Path

Path("src/main/java/com/challengecore/entity/ChallengeBossEntity.java").write_text(r'''package com.challengecore.entity;

import com.challengecore.network.ModNetwork;
import com.challengecore.network.packet.BossSwordOverlayPacket;
import com.challengecore.registry.ModSounds;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraftforge.network.PacketDistributor;
import org.joml.Vector3f;

public class ChallengeBossEntity extends Monster {
    private static final EntityDataAccessor<Integer> ATTACK_STATE=SynchedEntityData.defineId(ChallengeBossEntity.class,EntityDataSerializers.INT);
    private int specialCooldown=80,rayShots=0,rayDelay=0,swordHits=0,swordDelay=0,stateTicks=0;

    public ChallengeBossEntity(EntityType<? extends Monster> type,Level level){super(type,level);xpReward=100;}

    @Override protected void defineSynchedData(){super.defineSynchedData();entityData.define(ATTACK_STATE,0);}
    public int getAttackState(){return entityData.get(ATTACK_STATE);}
    private void setAttackState(int state,int ticks){entityData.set(ATTACK_STATE,state);stateTicks=ticks;}

    public static AttributeSupplier.Builder attributes(){
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH,300.0)
                .add(Attributes.ATTACK_DAMAGE,1.0)
                .add(Attributes.MOVEMENT_SPEED,0.27)
                .add(Attributes.ARMOR,12.0)
                .add(Attributes.KNOCKBACK_RESISTANCE,0.75)
                .add(Attributes.FOLLOW_RANGE,56.0);
    }

    @Override protected void registerGoals(){
        goalSelector.addGoal(0,new FloatGoal(this));
        goalSelector.addGoal(2,new MeleeAttackGoal(this,1.18,true));
        goalSelector.addGoal(6,new RandomStrollGoal(this,0.8));
        goalSelector.addGoal(7,new LookAtPlayerGoal(this,Player.class,20f));
        targetSelector.addGoal(1,new HurtByTargetGoal(this));
        targetSelector.addGoal(2,new NearestAttackableTargetGoal<>(this,Player.class,true));
    }

    @Override public void aiStep(){
        super.aiStep();
        if(level().isClientSide)return;

        if(stateTicks>0&&--stateTicks<=0&&rayShots<=0&&swordHits<=0)entityData.set(ATTACK_STATE,0);

        if(rayShots>0){
            if(--rayDelay<=0){doRay();rayShots--;rayDelay=14;}
            if(rayShots<=0)stateTicks=10;
            return;
        }

        if(swordHits>0){
            if(--swordDelay<=0){doSwordHit();swordHits--;swordDelay=10;}
            if(swordHits<=0)stateTicks=12;
            return;
        }

        if(--specialCooldown<=0){
            var target=getTarget();
            if(target!=null&&target.isAlive()){
                int pick=random.nextInt(3);
                if(pick==0){
                    setAttackState(1,55);
                    rayShots=3;rayDelay=4;
                }else if(pick==1){
                    setAttackState(2,45);
                    target.addEffect(new MobEffectInstance(MobEffects.WITHER,300,1));
                }else{
                    setAttackState(3,110);
                    swordHits=9;swordDelay=5;
                    if(target instanceof ServerPlayer sp)
                        ModNetwork.CHANNEL.send(PacketDistributor.PLAYER.with(()->sp),new BossSwordOverlayPacket(180));
                }
            }
            specialCooldown=120+random.nextInt(100);
        }
    }

    private void doRay(){
        var t=getTarget();if(t==null||!t.isAlive())return;
        if(level() instanceof ServerLevel sl){
            double sx=getX(),sy=getEyeY(),sz=getZ(),ex=t.getX(),ey=t.getEyeY(),ez=t.getZ();
            for(int i=0;i<=40;i++){
                double q=i/40d;
                sl.sendParticles(new DustParticleOptions(new Vector3f(1f,.01f,.01f),1.9f),
                        sx+(ex-sx)*q,sy+(ey-sy)*q,sz+(ez-sz)*q,2,.02,.02,.02,0);
            }
        }
        t.hurt(level().damageSources().mobAttack(this),8f);
        t.setSecondsOnFire(7);
    }

    private void doSwordHit(){
        var t=getTarget();if(t==null||!t.isAlive())return;
        float dmg=swordHits==1?2f:6f;
        t.hurt(level().damageSources().mobAttack(this),dmg);
    }

    @Override protected SoundEvent getAmbientSound(){return ModSounds.BOSS_BREATH.get();}
    @Override protected SoundEvent getHurtSound(DamageSource source){return null;}
    @Override protected SoundEvent getDeathSound(){return null;}
}
''')

Path("src/main/java/com/challengecore/client/render/ChallengeBossModel.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.entity.ChallengeBossEntity;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

public class ChallengeBossModel extends HierarchicalModel<ChallengeBossEntity> {
    private final ModelPart root,head,leftArm,rightArm,leftLeg,rightLeg,sword;
    public ChallengeBossModel(ModelPart root){
        this.root=root;
        head=root.getChild("head");
        leftArm=root.getChild("left_arm");
        rightArm=root.getChild("right_arm");
        leftLeg=root.getChild("left_leg");
        rightLeg=root.getChild("right_leg");
        sword=rightArm.getChild("sword");
    }

    public static LayerDefinition createBodyLayer(){
        MeshDefinition mesh=new MeshDefinition();PartDefinition r=mesh.getRoot();
        PartDefinition torso=r.addOrReplaceChild("torso",
                CubeListBuilder.create()
                        .texOffs(0,36).addBox(-7,-10,-4,14,17,8,new CubeDeformation(.25f))
                        .texOffs(48,36).addBox(-8,-8,-5,16,5,10,new CubeDeformation(.35f)),
                PartPose.offset(0,7,0));
        torso.addOrReplaceChild("waist",CubeListBuilder.create().texOffs(0,66).addBox(-7,-1,-4,14,5,8,new CubeDeformation(.15f)),PartPose.offset(0,6,0));

        PartDefinition head=r.addOrReplaceChild("head",
                CubeListBuilder.create()
                        .texOffs(0,0).addBox(-5,-6,-5,10,10,10,new CubeDeformation(.1f))
                        .texOffs(40,0).addBox(-6,-7,-6,12,4,12,new CubeDeformation(.2f))
                        .texOffs(40,18).addBox(-6,-3,-6.4f,12,4,2,new CubeDeformation(.05f)),
                PartPose.offset(0,-8,0));
        head.addOrReplaceChild("crest",CubeListBuilder.create().texOffs(84,0).addBox(-1,-8,-1,2,8,2),PartPose.offset(0,-6,0));
        head.addOrReplaceChild("horn_l",CubeListBuilder.create().texOffs(92,0).addBox(0,-1,-1,7,2,2),PartPose.offsetAndRotation(4,-7,0,0,0,-.55f));
        head.addOrReplaceChild("horn_r",CubeListBuilder.create().texOffs(92,0).mirror().addBox(-7,-1,-1,7,2,2),PartPose.offsetAndRotation(-4,-7,0,0,0,.55f));

        r.addOrReplaceChild("left_arm",
                CubeListBuilder.create()
                        .texOffs(0,82).addBox(0,-3,-3,5,18,6,new CubeDeformation(.15f))
                        .texOffs(24,82).addBox(-1,-5,-5,8,6,10,new CubeDeformation(.25f)),
                PartPose.offset(7,-1,0));

        PartDefinition rightArm=r.addOrReplaceChild("right_arm",
                CubeListBuilder.create()
                        .texOffs(0,82).mirror().addBox(-5,-3,-3,5,18,6,new CubeDeformation(.15f))
                        .texOffs(24,82).mirror().addBox(-7,-5,-5,8,6,10,new CubeDeformation(.25f)),
                PartPose.offset(-7,-1,0));

        rightArm.addOrReplaceChild("sword",
                CubeListBuilder.create()
                        .texOffs(64,62).addBox(-1,-2,-1,2,17,2)
                        .texOffs(76,62).addBox(-1.5f,14,-1.5f,3,9,3)
                        .texOffs(88,62).addBox(-4,12,-1,8,2,2),
                PartPose.offsetAndRotation(-2,10,-1,-.15f,0,0));

        r.addOrReplaceChild("left_leg",CubeListBuilder.create().texOffs(52,82).addBox(-2,-1,-2,5,15,5,new CubeDeformation(.1f)),PartPose.offset(3,13,0));
        r.addOrReplaceChild("right_leg",CubeListBuilder.create().texOffs(52,82).mirror().addBox(-3,-1,-2,5,15,5,new CubeDeformation(.1f)),PartPose.offset(-3,13,0));
        return LayerDefinition.create(mesh,128,128);
    }

    @Override public ModelPart root(){return root;}

    @Override public void setupAnim(ChallengeBossEntity e,float limbSwing,float limbAmount,float age,float yaw,float pitch){
        head.yRot=yaw*((float)Math.PI/180f);
        head.xRot=pitch*((float)Math.PI/180f);
        rightArm.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.0f*limbAmount;
        leftArm.xRot=(float)Math.cos(limbSwing*.6662)*1.0f*limbAmount;
        rightLeg.xRot=(float)Math.cos(limbSwing*.6662)*1.2f*limbAmount;
        leftLeg.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.2f*limbAmount;
        rightArm.yRot=rightArm.zRot=leftArm.yRot=leftArm.zRot=0;
        sword.visible=false;

        int state=e.getAttackState();
        if(state==1){
            float pulse=(float)Math.sin(age*.45f)*.08f;
            rightArm.xRot=-1.45f+pulse;leftArm.xRot=-1.45f-pulse;
            rightArm.yRot=-.18f;leftArm.yRot=.18f;
        }else if(state==2){
            rightArm.xRot=-2.25f;leftArm.xRot=-2.25f;
            rightArm.zRot=-.35f;leftArm.zRot=.35f;
        }else if(state==3){
            sword.visible=true;
            float stab=(float)Math.sin(age*.65f);
            rightArm.xRot=-1.65f+stab*.45f;rightArm.yRot=-.22f;leftArm.xRot=-.35f;
        }
    }
}
''')

Path("src/main/java/com/challengecore/client/render/ChallengeBossRenderer.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.ChallengeCore;
import com.challengecore.entity.ChallengeBossEntity;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

public class ChallengeBossRenderer extends MobRenderer<ChallengeBossEntity,ChallengeBossModel> {
    public static final ModelLayerLocation LAYER=new ModelLayerLocation(new ResourceLocation(ChallengeCore.MODID,"crimson_boss"),"main");
    private static final ResourceLocation TEX=new ResourceLocation(ChallengeCore.MODID,"textures/entity/crimson_boss.png");
    public ChallengeBossRenderer(EntityRendererProvider.Context ctx){super(ctx,new ChallengeBossModel(ctx.bakeLayer(LAYER)),1.25f);}
    @Override protected void scale(ChallengeBossEntity e,PoseStack pose,float partial){pose.scale(1.65f,1.65f,1.65f);}
    @Override public ResourceLocation getTextureLocation(ChallengeBossEntity e){return TEX;}
}
''')

# Bigger-than-Warden collision box
p=Path("src/main/java/com/challengecore/registry/ModEntities.java")
p.write_text(p.read_text().replace(".sized(1.4f,3.4f)",".sized(1.65f,4.25f)"))

# Roulette lasts 7.5 seconds
p=Path("src/main/java/com/challengecore/client/ClientState.java")
p.write_text(p.read_text().replace("rouletteTicks=180","rouletteTicks=150"))

# Replace the roulette renderer with the Dedsafio-style wheel and FIX texture UV dimensions.
p=Path("src/main/java/com/challengecore/client/ClientEvents.java")
s=p.read_text()
start=s.index("            if(ClientState.rouletteTicks>0){")
end=s.index("            lastRoulette=ClientState.rouletteTicks;",start)
new=r'''            if(ClientState.rouletteTicks>0){
                if(lastRoulette==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.ROULETTE_SPIN.get(),1f));
                int size=(int)(Math.min(w,h)*0.54f);
                float elapsed=150-ClientState.rouletteTicks;
                float progress=Math.min(1f,elapsed/118f);
                float eased=1f-(float)Math.pow(1f-progress,4);
                float pointerAngle=225f;
                float segment=45f;
                float resultAngle=Math.floorMod(ClientState.rouletteOutcome,8)*segment;
                float target=1980f+pointerAngle-resultAngle;
                float rot=target*eased;
                float intro=Math.min(1f,elapsed/8f);
                float outro=Math.min(1f,ClientState.rouletteTicks/12f);
                float scale=Math.min(intro,outro);
                RenderSystem.enableBlend();
                g.pose().pushPose();
                g.pose().translate(w/2f,h/2f,0);
                g.pose().scale(scale,scale,1);
                g.pose().mulPose(Axis.ZP.rotationDegrees(rot));
                g.blit(WHEEL_TEX,-size/2,-size/2,0,0,size,size,512,512);
                g.pose().popPose();

                int pw=Math.max(50,size/4),ph=Math.max(50,size/4);
                int px=(int)(w/2f-size/2f-pw*.42f);
                int py=(int)(h/2f-size*.36f);
                g.blit(POINTER_TEX,px,py,0,0,pw,ph,180,180);
                RenderSystem.disableBlend();

                if(ClientState.rouletteTicks<26){
                    String[] names={"VERDE","AMARILLO","NARANJA","ROJO","ROSA","MORADO","AZUL","CIAN"};
                    g.drawCenteredString(Minecraft.getInstance().font,names[Math.floorMod(ClientState.rouletteOutcome,names.length)],w/2,h/2+size/2+8,0xFFFFFFFF);
                }
            }
'''
p.write_text(s[:start]+new+s[end:])
