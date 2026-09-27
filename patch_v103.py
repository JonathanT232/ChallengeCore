from pathlib import Path
import base64, json

# v1.0.3
p=Path("build.gradle")
s=p.read_text().replace("version = '1.0.2'","version = '1.0.3'").replace("version = '1.0.1'","version = '1.0.3'")
p.write_text(s)

# Rat jackpot symbol, cropped from the user's supplied logo (no text).
rat = base64.b64decode("""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[...]""")
Path("src/main/resources/assets/challengecore/textures/item/symbol_rat.png").write_bytes(rat)

# Custom casino: stick, emerald, diamond, golden apple, rat jackpot.
Path("src/main/java/com/challengecore/client/render/SlotMachineRenderer.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.blockentity.SlotMachineBlockEntity;
import com.challengecore.registry.ModItems;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.joml.Quaternionf;

public class SlotMachineRenderer implements BlockEntityRenderer<SlotMachineBlockEntity> {
    public SlotMachineRenderer(BlockEntityRendererProvider.Context ctx){}
    private static Item symbol(int i){return switch(i){case 0->Items.STICK;case 1->Items.EMERALD;case 2->Items.DIAMOND;case 3->Items.GOLDEN_APPLE;default->ModItems.SYMBOL_RAT.get();};}
    @Override public void render(SlotMachineBlockEntity be,float partial,PoseStack pose,MultiBufferSource buf,int light,int overlay){
        for(int i=0;i<3;i++){
            pose.pushPose();
            pose.translate(.31+i*.19,1.13,.085);
            pose.mulPose(new Quaternionf().rotationY((float)Math.toRadians(180)));
            pose.scale(.43f,.43f,.43f);
            Minecraft.getInstance().getItemRenderer().renderStatic(new ItemStack(symbol(be.getDisplayResult(i))),ItemDisplayContext.GUI,light,OverlayTexture.NO_OVERLAY,pose,buf,be.getLevel(),i);
            pose.popPose();
        }
    }
}
''')

Path("src/main/java/com/challengecore/blockentity/SlotMachineBlockEntity.java").write_text(r'''package com.challengecore.blockentity;

import com.challengecore.menu.SlotConfigMenu;
import com.challengecore.registry.ModBlockEntities;
import com.challengecore.registry.ModItems;
import com.challengecore.registry.ModSounds;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.network.Connection;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.FireworkRocketEntity;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

public class SlotMachineBlockEntity extends BlockEntity implements MenuProvider {
    private final int[] result={0,0,0};
    private final Map<Integer,ItemStack> prizes=new HashMap<>();
    private final Random random=new Random();
    private int spinTicks=0;
    private UUID pendingPlayer=null;

    public SlotMachineBlockEntity(BlockPos p,BlockState s){super(ModBlockEntities.SLOT_MACHINE.get(),p,s);}

    public void spin(Player player){
        if(spinTicks>0)return;
        spinTicks=62;
        pendingPlayer=player.getUUID();
        for(int i=0;i<3;i++) result[i]=random.nextInt(5);
        setChanged();sync();
    }

    private ItemStack defaultPrize(int key){
        int rat=key(4,4,4);if(key==rat)return new ItemStack(ModItems.BLACK_CHIP.get(),5);
        int a=key/25,b=(key/5)%5,c=key%5;
        if(a==b&&b==c)return new ItemStack(ModItems.GOLD_CHIP.get(),2);
        if(a==b||a==c||b==c)return new ItemStack(ModItems.RED_CHIP.get(),3);
        return ItemStack.EMPTY;
    }

    private void resolve(ServerLevel level){
        if(pendingPlayer==null)return;
        ServerPlayer sp=level.getServer().getPlayerList().getPlayer(pendingPlayer);
        pendingPlayer=null;
        if(sp==null)return;
        int k=key(result[0],result[1],result[2]);
        ItemStack prize=prizes.getOrDefault(k,defaultPrize(k));
        if(!prize.isEmpty()){
            ItemStack give=prize.copy();
            if(!sp.addItem(give))sp.drop(give,false);
            level.playSound(null,worldPosition,ModSounds.SLOT_WIN.get(),net.minecraft.sounds.SoundSource.BLOCKS,1.2f,1f);
        }
        if(k==key(4,4,4)){
            for(int n=0;n<7;n++){
                ItemStack rocket=new ItemStack(Items.FIREWORK_ROCKET);
                CompoundTag fw=new CompoundTag();
                fw.putByte("Flight",(byte)1);
                ListTag exps=new ListTag();
                CompoundTag ex=new CompoundTag();
                ex.putByte("Type",(byte)(n%3));
                ex.putIntArray("Colors",new int[]{0xFFD21A,0xFF6B00,0xFFFFFF});
                ex.putBoolean("Flicker",true);
                ex.putBoolean("Trail",true);
                exps.add(ex);fw.put("Explosions",exps);
                rocket.getOrCreateTag().put("Fireworks",fw);
                FireworkRocketEntity ent=new FireworkRocketEntity(level,worldPosition.getX()+.5+(random.nextDouble()-.5)*1.5,worldPosition.getY()+1.2,worldPosition.getZ()+.5+(random.nextDouble()-.5)*1.5,rocket);
                level.addFreshEntity(ent);
            }
        }
    }

    public static int key(int a,int b,int c){return a*25+b*5+c;}
    public int getResult(int i){return result[i];}
    public int getDisplayResult(int i){
        if(spinTicks>0&&level!=null){
            int speed=spinTicks>34?1:spinTicks>16?2:3;
            return Math.floorMod((int)(level.getGameTime()/speed)+i*2,5);
        }
        return result[i];
    }
    public boolean isSpinning(){return spinTicks>0;}

    public static void tick(net.minecraft.world.level.Level level,net.minecraft.core.BlockPos pos,net.minecraft.world.level.block.state.BlockState state,SlotMachineBlockEntity be){
        if(be.spinTicks>0){
            be.spinTicks--;
            if(be.spinTicks==0){
                if(level instanceof ServerLevel sl)be.resolve(sl);
                be.sync();
            }else if(be.spinTicks%4==0)be.sync();
        }
    }

    public ItemStack getPrize(int key){return prizes.getOrDefault(key,ItemStack.EMPTY).copy();}
    public void setPrize(int key,ItemStack stack){if(stack.isEmpty())prizes.remove(key);else prizes.put(key,stack.copy());setChanged();sync();}
    private void sync(){if(level!=null)level.sendBlockUpdated(worldPosition,getBlockState(),getBlockState(),3);}

    @Override protected void saveAdditional(CompoundTag tag){
        super.saveAdditional(tag);tag.putIntArray("result",result);tag.putInt("spinTicks",spinTicks);
        if(pendingPlayer!=null)tag.putUUID("pendingPlayer",pendingPlayer);
        ListTag list=new ListTag();
        prizes.forEach((k,v)->{CompoundTag t=new CompoundTag();t.putInt("k",k);t.put("v",v.save(new CompoundTag()));list.add(t);});
        tag.put("prizes",list);
    }
    @Override public void load(CompoundTag tag){
        super.load(tag);int[] r=tag.getIntArray("result");if(r.length==3)System.arraycopy(r,0,result,0,3);
        spinTicks=tag.getInt("spinTicks");pendingPlayer=tag.hasUUID("pendingPlayer")?tag.getUUID("pendingPlayer"):null;
        prizes.clear();ListTag list=tag.getList("prizes",10);
        for(int i=0;i<list.size();i++){CompoundTag t=list.getCompound(i);prizes.put(t.getInt("k"),ItemStack.of(t.getCompound("v")));}
    }
    @Override public CompoundTag getUpdateTag(){return saveWithoutMetadata();}
    @Nullable @Override public ClientboundBlockEntityDataPacket getUpdatePacket(){return ClientboundBlockEntityDataPacket.create(this);}
    @Override public void onDataPacket(Connection net,ClientboundBlockEntityDataPacket pkt){CompoundTag tag=pkt.getTag();if(tag!=null)load(tag);}
    @Override public Component getDisplayName(){return Component.translatable("block.challengecore.slot_machine");}
    @Nullable @Override public AbstractContainerMenu createMenu(int id,Inventory inv,Player p){return new SlotConfigMenu(id,inv,this);}
}
''')

p=Path("src/main/java/com/challengecore/client/screen/SlotConfigScreen.java")
s=p.read_text().replace('private static final String[] SYMBOLS={"7","Diamante","Queso","Estrella","Rata"};',
                        'private static final String[] SYMBOLS={"Palo","Esmeralda","Diamante","Manzana dorada","Rata JACKPOT"};')
p.write_text(s)

# Large upright arcade cabinet, visually ~2 blocks tall.
Path("src/main/resources/assets/challengecore/models/block/slot_machine.json").write_text(r'''{
  "parent":"block/block",
  "textures":{"body":"challengecore:block/slot_body","gold":"challengecore:block/slot_gold","reel":"challengecore:block/slot_reel","particle":"challengecore:block/slot_body"},
  "elements":[
    {"from":[-2,0,2],"to":[18,9,15],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#body"}}},
    {"from":[-3,8,1],"to":[19,13,15],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[-1,13,4],"to":[17,29,15],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[0,24,2.7],"to":[16,28,4],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[0,15,2.3],"to":[16,23.5,4],"faces":{"north":{"texture":"#reel"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#body"}}},
    {"from":[-1,9.5,0.8],"to":[17,13,4],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#body"}}},
    {"from":[8.5,10.2,0],"to":[13.5,12.7,1.2],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[18,11,7],"to":[20,23,10],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#gold"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[19.5,20,7.4],"to":[22,23,9.6],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#gold"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#gold"},"down":{"texture":"#gold"}}}
  ],
  "display":{"gui":{"rotation":[30,225,0],"translation":[0,-3,0],"scale":[0.52,0.52,0.52]}}
}''')

# Bigger ATM physical model.
Path("src/main/resources/assets/challengecore/models/block/atm.json").write_text(r'''{
  "parent":"block/block",
  "textures":{"body":"challengecore:block/atm_body","dark":"challengecore:block/atm_dark","screen":"challengecore:block/atm_screen","particle":"challengecore:block/atm_body"},
  "elements":[
    {"from":[-2,0,2],"to":[18,28,15],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[-1,16,0.7],"to":[17,27,4],"rotation":{"origin":[8,16,4],"axis":"x","angle":-22.5},"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[1,18,0],"to":[15,25,1.1],"rotation":{"origin":[8,16,4],"axis":"x","angle":-22.5},"faces":{"north":{"texture":"#screen"},"south":{"texture":"#dark"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
    {"from":[-1,10,0.6],"to":[17,16,4],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[1,11,0],"to":[10,13.1,1],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#dark"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
    {"from":[11,10.8,0.1],"to":[16,15,2],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[1,5,0.2],"to":[14,8.5,2],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}}
  ],
  "display":{"gui":{"rotation":[30,225,0],"translation":[0,-3,0],"scale":[0.54,0.54,0.54]}}
}''')

# ATM GUI a little larger.
Path("src/main/java/com/challengecore/client/screen/AtmScreen.java").write_text(r'''package com.challengecore.client.screen;

import com.challengecore.menu.AtmMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;

public class AtmScreen extends AbstractContainerScreen<AtmMenu> {
    public AtmScreen(AtmMenu menu,Inventory inv,Component title){
        super(menu,inv,title);imageWidth=288;imageHeight=236;inventoryLabelY=123;inventoryLabelX=63;titleLabelX=12;titleLabelY=8;
    }
    @Override protected void renderBg(GuiGraphics g,float pt,int mx,int my){
        int x=(width-imageWidth)/2,y=(height-imageHeight)/2;
        g.fill(x,y,x+imageWidth,y+imageHeight,0xF0101318);
        g.fill(x+4,y+4,x+imageWidth-4,y+imageHeight-4,0xFF343B43);
        g.fill(x+12,y+27,x+imageWidth-12,y+113,0xFF0B1116);
        g.fill(x+20,y+35,x+imageWidth-20,y+105,0xFF18353A);
        g.drawCenteredString(font,"CAJERO CHALLENGE",x+imageWidth/2,y+12,0xFFFFFFFF);
        g.drawString(font,"MONEDA",x+62,y+45,0xFFC8FFF2,false);
        g.drawString(font,"FICHAS",x+180,y+45,0xFFC8FFF2,false);
        g.fill(x+84,y+53,x+110,y+79,0xFF303A45);
        g.fill(x+176,y+53,x+202,y+79,0xFF303A45);
        g.drawCenteredString(font,"BRONCE $1  ->  1 FICHA ROJA",x+imageWidth/2,y+82,0xFFFF5151);
        g.drawCenteredString(font,"PLATA $10  ->  10 FICHAS DORADAS",x+imageWidth/2,y+93,0xFFFFD54A);
        g.drawCenteredString(font,"ORO $100  ->  100 FICHAS NEGRAS",x+imageWidth/2,y+104,0xFFFFFFFF);
        g.fill(x+54,y+122,x+234,y+222,0xCC14181E);
    }
    @Override protected void renderLabels(GuiGraphics g,int mx,int my){
        g.drawString(font,title,titleLabelX,titleLabelY,0xFFEAEAEA,false);
        g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xFFBFC5CC,false);
    }
    @Override public void render(GuiGraphics g,int mx,int my,float pt){renderBackground(g);super.render(g,mx,my,pt);renderTooltip(g,mx,my);}
}
''')

# Move ATM slots/inventory to match larger UI.
p=Path("src/main/java/com/challengecore/menu/AtmMenu.java")
s=p.read_text()
s=s.replace("73,57","84,57").replace("165,57","176,57")
s=s.replace("47+c*18,124+r*18","63+c*18,136+r*18").replace("47+c*18,182","63+c*18,194")
p.write_text(s)

# New boss model silhouette: larger samurai, shoulder guards, back mantle, huge sword over shoulder.
Path("src/main/java/com/challengecore/client/render/ChallengeBossModel.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.entity.ChallengeBossEntity;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;

public class ChallengeBossModel extends HierarchicalModel<ChallengeBossEntity> {
    private final ModelPart root,head,leftArm,rightArm,leftLeg,rightLeg,sword,backSword;
    public ChallengeBossModel(ModelPart root){
        this.root=root;head=root.getChild("head");leftArm=root.getChild("left_arm");rightArm=root.getChild("right_arm");
        leftLeg=root.getChild("left_leg");rightLeg=root.getChild("right_leg");sword=rightArm.getChild("sword");backSword=root.getChild("back_sword");
    }
    public static LayerDefinition createBodyLayer(){
        MeshDefinition mesh=new MeshDefinition();PartDefinition r=mesh.getRoot();

        PartDefinition torso=r.addOrReplaceChild("torso",
          CubeListBuilder.create().texOffs(0,32).addBox(-7,-10,-4,14,18,8,new CubeDeformation(.35f))
            .texOffs(48,32).addBox(-8,-7,-5,16,5,10,new CubeDeformation(.35f))
            .texOffs(0,54).addBox(-6,-1,-5,12,10,10,new CubeDeformation(.15f)),
          PartPose.offset(0,5,0));
        torso.addOrReplaceChild("chest_plate",CubeListBuilder.create().texOffs(48,50).addBox(-5,-8,-1,10,11,2,new CubeDeformation(.25f)),PartPose.offset(0,0,-4.3f));
        torso.addOrReplaceChild("waist",CubeListBuilder.create().texOffs(0,76).addBox(-7,-1,-4,14,5,8,new CubeDeformation(.2f)),PartPose.offset(0,8,0));

        PartDefinition head=r.addOrReplaceChild("head",
          CubeListBuilder.create().texOffs(0,0).addBox(-5,-6,-5,10,10,10,new CubeDeformation(.15f))
            .texOffs(40,0).addBox(-6,-8,-6,12,5,12,new CubeDeformation(.25f))
            .texOffs(40,20).addBox(-6,-3,-6.5f,12,4,2,new CubeDeformation(.08f)),
          PartPose.offset(0,-9,0));
        head.addOrReplaceChild("crest",CubeListBuilder.create().texOffs(82,0).addBox(-1,-13,-1,2,13,2,new CubeDeformation(.1f)),PartPose.offset(0,-5,0));
        head.addOrReplaceChild("crest_tip",CubeListBuilder.create().texOffs(90,0).addBox(-1,-7,-1,2,8,2),PartPose.offsetAndRotation(0,-17,0,0,0,.6f));
        head.addOrReplaceChild("horn_l",CubeListBuilder.create().texOffs(100,0).addBox(0,-1,-1,8,2,2),PartPose.offsetAndRotation(4,-8,0,0,0,-.65f));
        head.addOrReplaceChild("horn_r",CubeListBuilder.create().texOffs(100,0).mirror().addBox(-8,-1,-1,8,2,2),PartPose.offsetAndRotation(-4,-8,0,0,0,.65f));

        PartDefinition la=r.addOrReplaceChild("left_arm",
          CubeListBuilder.create().texOffs(0,92).addBox(0,-3,-3,5,19,6,new CubeDeformation(.18f))
            .texOffs(24,92).addBox(-1,-6,-6,9,7,12,new CubeDeformation(.32f)),
          PartPose.offset(7,-2,0));
        la.addOrReplaceChild("shoulder_spike",CubeListBuilder.create().texOffs(70,88).addBox(0,-2,-2,8,3,4),PartPose.offsetAndRotation(4,-5,0,0,0,-.45f));

        PartDefinition ra=r.addOrReplaceChild("right_arm",
          CubeListBuilder.create().texOffs(0,92).mirror().addBox(-5,-3,-3,5,19,6,new CubeDeformation(.18f))
            .texOffs(24,92).mirror().addBox(-8,-6,-6,9,7,12,new CubeDeformation(.32f)),
          PartPose.offset(-7,-2,0));
        ra.addOrReplaceChild("shoulder_spike",CubeListBuilder.create().texOffs(70,88).mirror().addBox(-8,-2,-2,8,3,4),PartPose.offsetAndRotation(-4,-5,0,0,0,.45f));

        ra.addOrReplaceChild("sword",
          CubeListBuilder.create().texOffs(76,52).addBox(-1,-3,-1,2,25,2)
            .texOffs(88,52).addBox(-2,19,-2,4,11,4)
            .texOffs(104,52).addBox(-6,17,-1,12,2,2),
          PartPose.offsetAndRotation(-2,9,-1,-.18f,0,0));

        r.addOrReplaceChild("back_sword",
          CubeListBuilder.create().texOffs(76,52).addBox(-1,-3,-1,2,29,2)
            .texOffs(88,52).addBox(-2,23,-2,4,12,4)
            .texOffs(104,52).addBox(-6,21,-1,12,2,2),
          PartPose.offsetAndRotation(4,-10,4,-.55f,0,-.72f));

        PartDefinition mantle=r.addOrReplaceChild("mantle",CubeListBuilder.create().texOffs(64,98).addBox(-9,-2,-2,18,5,4,new CubeDeformation(.2f)),PartPose.offset(0,-3,4));
        for(int i=0;i<5;i++){
            mantle.addOrReplaceChild("feather"+i,CubeListBuilder.create().texOffs(96,98).addBox(-1,-1,0,2,10,2),PartPose.offsetAndRotation(-6+i*3,-1,1,.45f,0,(i-2)*.15f));
        }

        r.addOrReplaceChild("left_leg",CubeListBuilder.create().texOffs(52,76).addBox(-2,-1,-2,5,16,5,new CubeDeformation(.12f)),PartPose.offset(3,13,0));
        r.addOrReplaceChild("right_leg",CubeListBuilder.create().texOffs(52,76).mirror().addBox(-3,-1,-2,5,16,5,new CubeDeformation(.12f)),PartPose.offset(-3,13,0));
        return LayerDefinition.create(mesh,128,128);
    }
    @Override public ModelPart root(){return root;}
    @Override public void setupAnim(ChallengeBossEntity e,float limbSwing,float limbAmount,float age,float yaw,float pitch){
        head.yRot=yaw*((float)Math.PI/180f);head.xRot=pitch*((float)Math.PI/180f);
        rightArm.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.0f*limbAmount;
        leftArm.xRot=(float)Math.cos(limbSwing*.6662)*1.0f*limbAmount;
        rightLeg.xRot=(float)Math.cos(limbSwing*.6662)*1.15f*limbAmount;
        leftLeg.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.15f*limbAmount;
        rightArm.yRot=rightArm.zRot=leftArm.yRot=leftArm.zRot=0;sword.visible=false;backSword.visible=true;
        int state=e.getAttackState();
        if(state==1){float p=(float)Math.sin(age*.5f)*.1f;rightArm.xRot=-1.55f+p;leftArm.xRot=-1.55f-p;rightArm.yRot=-.25f;leftArm.yRot=.25f;}
        else if(state==2){rightArm.xRot=-2.15f;leftArm.xRot=-2.15f;rightArm.zRot=-.45f;leftArm.zRot=.45f;}
        else if(state==3){sword.visible=true;backSword.visible=false;float stab=(float)Math.sin(age*.7f);rightArm.xRot=-1.75f+stab*.5f;rightArm.yRot=-.25f;leftArm.xRot=-.3f;}
    }
}
''')

p=Path("src/main/java/com/challengecore/client/render/ChallengeBossRenderer.java")
s=p.read_text().replace("pose.scale(1.65f,1.65f,1.65f)","pose.scale(1.8f,1.8f,1.8f)")
p.write_text(s)

# Roulette: no matrix rotation. Uses a pre-rotated 32-frame atlas generated at build time.
p=Path("src/main/java/com/challengecore/client/ClientEvents.java")
s=p.read_text()
s=s.replace('private static final ResourceLocation WHEEL_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette.png");',
            'private static final ResourceLocation WHEEL_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette_atlas.png");')
start=s.index("            if(ClientState.rouletteTicks>0){")
end=s.index("            lastRoulette=ClientState.rouletteTicks;",start)
new=r'''            if(ClientState.rouletteTicks>0){
                if(lastRoulette==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.ROULETTE_SPIN.get(),1f));
                int size=(int)(Math.min(w,h)*0.58f);
                float elapsed=150-ClientState.rouletteTicks;
                float p=Math.min(1f,elapsed/120f);
                float ease=1f-(float)Math.pow(1f-p,4);
                int outcome=Math.floorMod(ClientState.rouletteOutcome,8);
                float targetTurns=5.5f*360f + outcome*45f;
                float angle=targetTurns*ease;
                int frame=Math.floorMod(Math.round(angle/11.25f),32);
                int u=(frame%8)*256,v=(frame/8)*256;
                float intro=Math.min(1f,elapsed/8f),outro=Math.min(1f,ClientState.rouletteTicks/10f);
                float scale=Math.min(intro,outro);
                int draw=(int)(size*scale),x=w/2-draw/2,y=h/2-draw/2;
                RenderSystem.enableBlend();
                g.blit(WHEEL_TEX,x,y,draw,draw,u,v,256,256,2048,1024);
                int pw=Math.max(54,(int)(size*.30f)),ph=pw;
                int px=w/2-size/2-(int)(pw*.32f),py=h/2-size/2+(int)(size*.08f);
                g.blit(POINTER_TEX,px,py,0,0,pw,ph,180,180);
                RenderSystem.disableBlend();
                if(ClientState.rouletteTicks<24){
                    String[] names={"VERDE","AMARILLO","NARANJA","ROJO","ROSA","MORADO","AZUL","CIAN"};
                    int[] cols={0xFF00D13B,0xFFFFD11A,0xFFFF9400,0xFFFF4545,0xFFFF48C8,0xFF9747E8,0xFF3555E8,0xFF23C6D6};
                    g.drawCenteredString(Minecraft.getInstance().font,names[outcome],w/2,h/2+size/2+9,cols[outcome]);
                }
            }
'''
s=s[:start]+new+s[end:]
p.write_text(s)

# Build-time Java asset generator: exact wheel frames + brighter black/orange boss texture.
Path("GenerateAssets103.java").write_text(r'''import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;

public class GenerateAssets103 {
  public static void main(String[] args) throws Exception {
    File wheelFile=new File("src/main/resources/assets/challengecore/textures/gui/roulette.png");
    BufferedImage src=ImageIO.read(wheelFile);
    int fs=256;
    BufferedImage atlas=new BufferedImage(fs*8,fs*4,BufferedImage.TYPE_INT_ARGB);
    Graphics2D ag=atlas.createGraphics();
    ag.setRenderingHint(RenderingHints.KEY_INTERPOLATION,RenderingHints.VALUE_INTERPOLATION_BICUBIC);
    for(int i=0;i<32;i++){
      BufferedImage fr=new BufferedImage(fs,fs,BufferedImage.TYPE_INT_ARGB);
      Graphics2D g=fr.createGraphics();
      g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,RenderingHints.VALUE_INTERPOLATION_BICUBIC);
      AffineTransform t=new AffineTransform();
      t.translate(fs/2.0,fs/2.0);
      t.rotate(Math.toRadians(-i*11.25));
      t.translate(-fs/2.0,-fs/2.0);
      t.scale(fs/(double)src.getWidth(),fs/(double)src.getHeight());
      g.drawImage(src,t,null);g.dispose();
      ag.drawImage(fr,(i%8)*fs,(i/8)*fs,null);
    }
    ag.dispose();
    ImageIO.write(atlas,"png",new File("src/main/resources/assets/challengecore/textures/gui/roulette_atlas.png"));

    BufferedImage boss=new BufferedImage(128,128,BufferedImage.TYPE_INT_ARGB);
    Graphics2D b=boss.createGraphics();
    b.setColor(new Color(16,17,19));b.fillRect(0,0,128,128);
    b.setColor(new Color(225,145,12));
    for(int y=0;y<128;y+=16)b.fillRect(0,y,128,3);
    b.setColor(new Color(95,54,10));
    for(int x=8;x<128;x+=24)b.fillRect(x,0,5,128);
    b.setColor(new Color(245,177,31));
    b.fillRect(3,3,25,17);b.fillRect(40,3,36,12);b.fillRect(0,34,44,8);b.fillRect(48,34,36,8);
    b.setColor(new Color(57,58,61));b.fillRect(92,65,28,30);
    b.setColor(new Color(255,104,18));b.fillRect(2,58,34,9);b.fillRect(50,56,26,9);
    b.setColor(new Color(245,210,80));b.fillRect(44,21,24,4);
    b.dispose();
    ImageIO.write(boss,"png",new File("src/main/resources/assets/challengecore/textures/entity/crimson_boss.png"));
  }
}
''')
