from pathlib import Path

# Version
p=Path("build.gradle")
s=p.read_text()
for old in ["1.0.4","1.0.3","1.0.2","1.0.1"]:
    s=s.replace("version = '"+old+"'","version = '1.0.5'")
p.write_text(s)

# ---------------- ATM: explicit conversion only, both directions ----------------
Path("src/main/java/com/challengecore/blockentity/AtmBlockEntity.java").write_text(r'''package com.challengecore.blockentity;

import com.challengecore.registry.ModBlockEntities;
import com.challengecore.registry.ModItems;
import net.minecraft.core.BlockPos;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.world.Container;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class AtmBlockEntity extends BlockEntity implements Container {
    private final NonNullList<ItemStack> items=NonNullList.withSize(2,ItemStack.EMPTY);

    public AtmBlockEntity(BlockPos p, BlockState s){super(ModBlockEntities.ATM.get(),p,s);}

    public boolean convert(){
        ItemStack in=items.get(0);
        if(in.isEmpty())return false;

        ItemStack result=ItemStack.EMPTY;
        int consume=0;

        if(in.is(ModItems.BRONZE_COIN.get())){
            int n=Math.min(in.getCount(),999);
            result=new ItemStack(ModItems.RED_CHIP.get(),n);consume=n;
        }else if(in.is(ModItems.SILVER_COIN.get())){
            int maxCoins=Math.min(in.getCount(),99);
            result=new ItemStack(ModItems.GOLD_CHIP.get(),maxCoins*10);consume=maxCoins;
        }else if(in.is(ModItems.GOLD_COIN.get())){
            int maxCoins=Math.min(in.getCount(),9);
            result=new ItemStack(ModItems.BLACK_CHIP.get(),maxCoins*100);consume=maxCoins;
        }else if(in.is(ModItems.CASINO_CHIP.get())||in.is(ModItems.RED_CHIP.get())){
            int n=Math.min(in.getCount(),999);
            result=new ItemStack(ModItems.BRONZE_COIN.get(),n);consume=n;
        }else if(in.is(ModItems.GOLD_CHIP.get())){
            int groups=in.getCount()/10;
            if(groups>0){result=new ItemStack(ModItems.SILVER_COIN.get(),groups);consume=groups*10;}
        }else if(in.is(ModItems.BLACK_CHIP.get())){
            int groups=in.getCount()/100;
            if(groups>0){result=new ItemStack(ModItems.GOLD_COIN.get(),groups);consume=groups*100;}
        }

        if(result.isEmpty()||consume<=0)return false;

        ItemStack out=items.get(1);
        int room;
        if(out.isEmpty()) room=Math.min(result.getMaxStackSize(),999);
        else if(ItemStack.isSameItemSameTags(out,result)) room=Math.min(out.getMaxStackSize(),999)-out.getCount();
        else return false;
        if(room<=0)return false;

        int perUnit=result.getCount()/Math.max(1,consume);
        if(perUnit>1){
            int maxConsume=room/perUnit;
            if(maxConsume<=0)return false;
            if(maxConsume<consume){
                consume=maxConsume;
                result.setCount(consume*perUnit);
            }
        }else if(result.getCount()>room){
            result.setCount(room);
            consume=room;
        }

        in.shrink(consume);
        if(in.isEmpty())items.set(0,ItemStack.EMPTY);
        if(out.isEmpty())items.set(1,result);
        else out.grow(result.getCount());
        setChanged();sync();
        return true;
    }

    private void sync(){if(level!=null)level.sendBlockUpdated(worldPosition,getBlockState(),getBlockState(),3);}
    @Override public int getContainerSize(){return 2;}
    @Override public boolean isEmpty(){return items.get(0).isEmpty()&&items.get(1).isEmpty();}
    @Override public ItemStack getItem(int i){return items.get(i);}
    @Override public ItemStack removeItem(int i,int amount){ItemStack s=ContainerHelper.removeItem(items,i,amount);if(!s.isEmpty()){setChanged();sync();}return s;}
    @Override public ItemStack removeItemNoUpdate(int i){ItemStack s=ContainerHelper.takeItem(items,i);setChanged();return s;}
    @Override public void setItem(int i,ItemStack stack){items.set(i,stack);setChanged();sync();}
    @Override public boolean stillValid(Player p){return level!=null&&level.getBlockEntity(worldPosition)==this&&p.distanceToSqr(worldPosition.getX()+.5,worldPosition.getY()+.5,worldPosition.getZ()+.5)<=64;}
    @Override public void clearContent(){items.clear();setChanged();sync();}
    @Override protected void saveAdditional(CompoundTag tag){super.saveAdditional(tag);ContainerHelper.saveAllItems(tag,items);}
    @Override public void load(CompoundTag tag){super.load(tag);ContainerHelper.loadAllItems(tag,items);}
    @Override public CompoundTag getUpdateTag(){return saveWithoutMetadata();}
    @Nullable @Override public ClientboundBlockEntityDataPacket getUpdatePacket(){return ClientboundBlockEntityDataPacket.create(this);}
    @Override public void onDataPacket(Connection net,ClientboundBlockEntityDataPacket pkt){if(pkt.getTag()!=null)load(pkt.getTag());}
}
''')

Path("src/main/java/com/challengecore/menu/AtmMenu.java").write_text(r'''package com.challengecore.menu;

import com.challengecore.blockentity.AtmBlockEntity;
import com.challengecore.registry.ModBlocks;
import com.challengecore.registry.ModItems;
import com.challengecore.registry.ModMenus;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

public class AtmMenu extends AbstractContainerMenu {
    private final AtmBlockEntity be;

    public AtmMenu(int id, Inventory inv, FriendlyByteBuf buf){this(id,inv,(AtmBlockEntity)inv.player.level().getBlockEntity(buf.readBlockPos()));}
    public AtmMenu(int id, Inventory inv, AtmBlockEntity be){
        super(ModMenus.ATM.get(),id);this.be=be;
        addSlot(new Slot(be,0,92,67){
            @Override public boolean mayPlace(ItemStack s){
                return s.is(ModItems.BRONZE_COIN.get())||s.is(ModItems.SILVER_COIN.get())||s.is(ModItems.GOLD_COIN.get())
                    ||s.is(ModItems.CASINO_CHIP.get())||s.is(ModItems.RED_CHIP.get())||s.is(ModItems.GOLD_CHIP.get())||s.is(ModItems.BLACK_CHIP.get());
            }
        });
        addSlot(new Slot(be,1,196,67){@Override public boolean mayPlace(ItemStack s){return false;}});
        for(int r=0;r<3;r++)for(int c=0;c<9;c++)addSlot(new Slot(inv,c+r*9+9,64+c*18,151+r*18));
        for(int c=0;c<9;c++)addSlot(new Slot(inv,c,64+c*18,209));
    }

    @Override public boolean clickMenuButton(Player p,int id){
        if(id==0 && !p.level().isClientSide)return be.convert();
        return false;
    }

    @Override public ItemStack quickMoveStack(Player p,int index){
        ItemStack ret=ItemStack.EMPTY;
        Slot slot=slots.get(index);
        if(slot==null||!slot.hasItem())return ret;
        ItemStack s=slot.getItem();ret=s.copy();
        if(index==0||index==1){
            if(!moveItemStackTo(s,2,38,true))return ItemStack.EMPTY;
        }else{
            if(!moveItemStackTo(s,0,1,false))return ItemStack.EMPTY;
        }
        if(s.isEmpty())slot.set(ItemStack.EMPTY);else slot.setChanged();
        return ret;
    }
    @Override public boolean stillValid(Player p){return be!=null&&stillValid(ContainerLevelAccess.create(be.getLevel(),be.getBlockPos()),p,ModBlocks.ATM.get());}
}
''')

Path("src/main/java/com/challengecore/client/screen/AtmScreen.java").write_text(r'''package com.challengecore.client.screen;

import com.challengecore.menu.AtmMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;

public class AtmScreen extends AbstractContainerScreen<AtmMenu> {
    public AtmScreen(AtmMenu menu,Inventory inv,Component title){
        super(menu,inv,title);imageWidth=304;imageHeight=258;inventoryLabelX=64;inventoryLabelY=139;titleLabelX=14;titleLabelY=9;
    }
    @Override protected void init(){
        super.init();
        addRenderableWidget(Button.builder(Component.literal("CAMBIAR"),b->{
            if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,0);
        }).bounds(leftPos+113,topPos+109,78,20).build());
    }
    @Override protected void renderBg(GuiGraphics g,float pt,int mx,int my){
        int x=leftPos,y=topPos;
        g.fill(x,y,x+imageWidth,y+imageHeight,0xF00B0E12);
        g.fill(x+4,y+4,x+imageWidth-4,y+imageHeight-4,0xFF343A42);
        g.fill(x+14,y+26,x+imageWidth-14,y+137,0xFF0B1116);
        g.fill(x+20,y+32,x+imageWidth-20,y+103,0xFF16343A);
        g.drawCenteredString(font,"CAJERO CHALLENGE",x+imageWidth/2,y+11,0xFFFFFFFF);
        g.drawCenteredString(font,"MONEDAS  ⇄  FICHAS",x+imageWidth/2,y+36,0xFFBFFCF1);
        g.drawString(font,"ENTRADA",x+71,y+55,0xFFFFFFFF,false);
        g.drawString(font,"SALIDA",x+179,y+55,0xFFFFFFFF,false);
        g.fill(x+88,y+63,x+116,y+91,0xFF29343D);
        g.fill(x+192,y+63,x+220,y+91,0xFF29343D);

        g.drawCenteredString(font,"1 BRONCE ⇄ 1 ROJA",x+imageWidth/2,y+93,0xFFFF5757);
        g.drawCenteredString(font,"1 PLATA ⇄ 10 DORADAS",x+imageWidth/2,y+103,0xFFFFD44A);
        g.drawCenteredString(font,"1 ORO ⇄ 100 NEGRAS",x+imageWidth/2,y+113,0xFFFFFFFF);
        g.drawCenteredString(font,"El cambio SOLO se hace al pulsar CAMBIAR",x+imageWidth/2,y+132,0xFF90E6DA);
        g.fill(x+54,y+144,x+250,y+247,0xCC151A20);
    }
    @Override protected void renderLabels(GuiGraphics g,int mx,int my){
        g.drawString(font,title,titleLabelX,titleLabelY,0xFFEAEAEA,false);
        g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xFFBFC5CC,false);
    }
    @Override public void render(GuiGraphics g,int mx,int my,float pt){renderBackground(g);super.render(g,mx,my,pt);renderTooltip(g,mx,my);}
}
''')

# ---------------- Slot machine: configured prizes ONLY ----------------
p=Path("src/main/java/com/challengecore/blockentity/SlotMachineBlockEntity.java")
s=p.read_text()
start=s.find("    private ItemStack defaultPrize")
if start>=0:
    end=s.find("    private void resolve",start)
    s=s[:start]+s[end:]
s=s.replace("ItemStack prize=prizes.getOrDefault(k,defaultPrize(k));","ItemStack prize=prizes.getOrDefault(k,ItemStack.EMPTY);")
p.write_text(s)

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
            // Centered precisely over the three white physical reels.
            pose.translate(.285+i*.215,1.245,.068);
            pose.mulPose(new Quaternionf().rotationY((float)Math.toRadians(180)));
            pose.scale(.245f,.245f,.245f);
            Minecraft.getInstance().getItemRenderer().renderStatic(new ItemStack(symbol(be.getDisplayResult(i))),ItemDisplayContext.GUI,light,OverlayTexture.NO_OVERLAY,pose,buf,be.getLevel(),i);
            pose.popPose();
        }
    }
}
''')

Path("src/main/java/com/challengecore/client/screen/SlotConfigScreen.java").write_text(r'''package com.challengecore.client.screen;

import com.challengecore.menu.SlotConfigMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;

public class SlotConfigScreen extends AbstractContainerScreen<SlotConfigMenu> {
    private static final String[] SYMBOLS={"Palo","Esmeralda","Diamante","Manzana dorada","Rata JACKPOT"};
    public SlotConfigScreen(SlotConfigMenu menu,Inventory inv,Component title){super(menu,inv,title);imageWidth=220;imageHeight=198;}
    @Override protected void init(){
        super.init();int x=leftPos,y=topPos;
        for(int i=0;i<3;i++){
            final int idx=i;
            addRenderableWidget(Button.builder(Component.literal("<"),b->press(idx*2+1)).bounds(x+18+i*66,y+25,18,18).build());
            addRenderableWidget(Button.builder(Component.literal(">"),b->press(idx*2)).bounds(x+50+i*66,y+25,18,18).build());
        }
        addRenderableWidget(Button.builder(Component.literal("Guardar premio"),b->press(6)).bounds(x+66,y+77,90,20).build());
    }
    private void press(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void renderBg(GuiGraphics g,float pt,int mx,int my){
        int x=leftPos,y=topPos;
        g.fill(x,y,x+imageWidth,y+imageHeight,0xF00A0A0C);
        g.fill(x+4,y+4,x+imageWidth-4,y+imageHeight-4,0xFF251B08);
        g.fill(x+10,y+12,x+imageWidth-10,y+70,0xFF111114);
        for(int i=0;i<3;i++){
            g.fill(x+13+i*66,y+20,x+73+i*66,y+63,0xFFF4F0E7);
            String ss=SYMBOLS[Math.floorMod(menu.sym(i),5)];
            g.drawCenteredString(font,ss,x+43+i*66,y+49,0xFF1B1110);
        }
        g.drawString(font,"Premio de esta combinación:",x+18,y+68,0xFFFFD34D,false);
        g.drawCenteredString(font,"Sin premio configurado = no entrega nada",x+imageWidth/2,y+101,0xFFBFBFBF);
    }
    @Override public void render(GuiGraphics g,int mx,int my,float pt){renderBackground(g);super.render(g,mx,my,pt);renderTooltip(g,mx,my);}
}
''')

# ---------------- Grill: fully functional food cooking ----------------
Path("src/main/java/com/challengecore/blockentity/GrillBlockEntity.java").write_text(r'''package com.challengecore.blockentity;

import com.challengecore.registry.ModBlockEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.particles.ParticleTypes;
import org.jetbrains.annotations.Nullable;

import java.util.Map;

public class GrillBlockEntity extends BlockEntity {
    private ItemStack food=ItemStack.EMPTY;
    private int cookTime=0,flipCount=0;
    private boolean cooked=false;
    public static final int TOTAL_COOK=200;

    private static final Map<Item,Item> COOKED=Map.ofEntries(
        Map.entry(Items.BEEF,Items.COOKED_BEEF),
        Map.entry(Items.PORKCHOP,Items.COOKED_PORKCHOP),
        Map.entry(Items.CHICKEN,Items.COOKED_CHICKEN),
        Map.entry(Items.MUTTON,Items.COOKED_MUTTON),
        Map.entry(Items.RABBIT,Items.COOKED_RABBIT),
        Map.entry(Items.COD,Items.COOKED_COD),
        Map.entry(Items.SALMON,Items.COOKED_SALMON),
        Map.entry(Items.POTATO,Items.BAKED_POTATO)
    );

    public GrillBlockEntity(BlockPos p,BlockState s){super(ModBlockEntities.GRILL.get(),p,s);}
    public static boolean canCook(ItemStack s){return !s.isEmpty()&&COOKED.containsKey(s.getItem());}
    public boolean isEmpty(){return food.isEmpty();}
    public boolean isCooked(){return cooked;}
    public int getCookTime(){return cookTime;}
    public int getFlipCount(){return flipCount;}
    public ItemStack getFood(){return food;}
    public float getProgress(){return Math.min(1f,cookTime/(float)TOTAL_COOK);}

    public void setFood(ItemStack stack){food=stack.copy();food.setCount(1);cookTime=0;flipCount=0;cooked=false;setChanged();sync();}
    public void flip(){if(!food.isEmpty()&&!cooked){flipCount++;setChanged();sync();}}
    public ItemStack takeFood(){ItemStack out=food.copy();food=ItemStack.EMPTY;cookTime=0;flipCount=0;cooked=false;setChanged();sync();return out;}
    public ItemStack cancelFood(){return takeFood();}

    public static void tick(Level level,BlockPos pos,BlockState state,GrillBlockEntity be){
        if(be.food.isEmpty()||be.cooked)return;
        if(!level.isClientSide){
            be.cookTime++;
            if(level instanceof ServerLevel sl){
                if(be.cookTime%8==0){
                    sl.sendParticles(ParticleTypes.SMOKE,pos.getX()+.5,pos.getY()+.88,pos.getZ()+.5,2,.24,.05,.24,.01);
                    if(be.cookTime>35)sl.sendParticles(ParticleTypes.FLAME,pos.getX()+.5,pos.getY()+.70,pos.getZ()+.5,1,.22,.03,.22,.005);
                }
                if(be.cookTime%45==0)sl.playSound(null,pos,SoundEvents.CAMPFIRE_CRACKLE,SoundSource.BLOCKS,.55f,.9f+level.random.nextFloat()*.2f);
            }
            if(be.cookTime>=TOTAL_COOK){
                Item out=COOKED.get(be.food.getItem());
                if(out!=null){be.food=new ItemStack(out);be.cooked=true;}
                be.setChanged();be.sync();
            }else if(be.cookTime%10==0)be.sync();
        }
    }
    private void sync(){if(level!=null)level.sendBlockUpdated(worldPosition,getBlockState(),getBlockState(),3);}
    @Override protected void saveAdditional(CompoundTag tag){super.saveAdditional(tag);if(!food.isEmpty())tag.put("food",food.save(new CompoundTag()));tag.putInt("cookTime",cookTime);tag.putInt("flipCount",flipCount);tag.putBoolean("cooked",cooked);}
    @Override public void load(CompoundTag tag){super.load(tag);food=tag.contains("food")?ItemStack.of(tag.getCompound("food")):ItemStack.EMPTY;cookTime=tag.getInt("cookTime");flipCount=tag.getInt("flipCount");cooked=tag.getBoolean("cooked");}
    @Override public CompoundTag getUpdateTag(){return saveWithoutMetadata();}
    @Nullable @Override public ClientboundBlockEntityDataPacket getUpdatePacket(){return ClientboundBlockEntityDataPacket.create(this);}
    @Override public void onDataPacket(Connection net,ClientboundBlockEntityDataPacket pkt){if(pkt.getTag()!=null)load(pkt.getTag());}
}
''')

Path("src/main/java/com/challengecore/block/GrillBlock.java").write_text(r'''package com.challengecore.block;

import com.challengecore.blockentity.GrillBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

public class GrillBlock extends BaseEntityBlock {
    private static final VoxelShape SHAPE=Shapes.or(
        Block.box(1,7,1,15,12,15),
        Block.box(2,0,2,4,8,4),Block.box(12,0,2,14,8,4),
        Block.box(2,0,12,4,8,14),Block.box(12,0,12,14,8,14)
    );
    public GrillBlock(Properties p){super(p);}
    @Override public VoxelShape getShape(BlockState s,BlockGetter g,BlockPos p,CollisionContext c){return SHAPE;}
    @Override public RenderShape getRenderShape(BlockState s){return RenderShape.MODEL;}
    @Nullable @Override public BlockEntity newBlockEntity(BlockPos p,BlockState s){return new GrillBlockEntity(p,s);}
    @Nullable @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type){return createTickerHelper(type,com.challengecore.registry.ModBlockEntities.GRILL.get(),GrillBlockEntity::tick);}
    @Override public InteractionResult use(BlockState state,Level level,BlockPos pos,Player player,InteractionHand hand,BlockHitResult hit){
        if(!(level.getBlockEntity(pos) instanceof GrillBlockEntity be))return InteractionResult.PASS;
        ItemStack held=player.getItemInHand(hand);
        if(!level.isClientSide){
            if(be.isEmpty()&&GrillBlockEntity.canCook(held)){
                ItemStack one=held.copy();one.setCount(1);be.setFood(one);
                if(!player.getAbilities().instabuild)held.shrink(1);
                player.displayClientMessage(Component.literal("Carne colocada en el asador."),true);
                return InteractionResult.CONSUME;
            }
            if(held.isEmpty()&&!be.isEmpty()){
                if(be.isCooked()){
                    ItemStack out=be.takeFood();
                    if(!player.addItem(out))player.drop(out,false);
                    player.displayClientMessage(Component.literal("Listo: comida cocinada."),true);
                }else{
                    be.flip();
                    player.displayClientMessage(Component.literal("Volteaste la comida."),true);
                }
                return InteractionResult.CONSUME;
            }
            if(player.isShiftKeyDown()&&!be.isEmpty()&&!be.isCooked()){
                ItemStack out=be.cancelFood();
                if(!player.addItem(out))player.drop(out,false);
                return InteractionResult.CONSUME;
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
}
''')

Path("src/main/java/com/challengecore/client/render/GrillRenderer.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.blockentity.GrillBlockEntity;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.item.ItemDisplayContext;
import org.joml.Quaternionf;

public class GrillRenderer implements BlockEntityRenderer<GrillBlockEntity> {
    public GrillRenderer(BlockEntityRendererProvider.Context ctx){}
    @Override public void render(GrillBlockEntity be,float partial,PoseStack pose,MultiBufferSource buf,int light,int overlay){
        if(be.getFood().isEmpty())return;
        pose.pushPose();
        pose.translate(.5,.79,.5);
        float base=(be.getFlipCount()%2)*180f;
        float flip=(!be.isCooked()&&be.getCookTime()%70<12)?((be.getCookTime()%70)+partial)/12f*180f:0f;
        pose.mulPose(new Quaternionf().rotationX((float)Math.toRadians(base+flip)));
        pose.mulPose(new Quaternionf().rotationY((float)Math.toRadians(18)));
        pose.scale(.68f,.68f,.68f);
        Minecraft.getInstance().getItemRenderer().renderStatic(be.getFood(),ItemDisplayContext.GROUND,light,OverlayTexture.NO_OVERLAY,pose,buf,be.getLevel(),0);
        pose.popPose();
    }
}
''')

# ---------------- Death & roulette timing/render ----------------
Path("src/main/java/com/challengecore/client/ClientState.java").write_text(r'''package com.challengecore.client;
public final class ClientState {
    public static final int DEATH_TOTAL=160;
    public static final int ROULETTE_TOTAL=296;
    public static final int ROULETTE_VISUAL_DELAY=5;
    public static int deathTicks=0,rouletteTicks=0,rouletteOutcome=0,swordTicks=0;
    public static String deadName="";
    public static void startDeath(String name){deadName=name;deathTicks=DEATH_TOTAL;}
    public static void startRoulette(int outcome){rouletteOutcome=Math.floorMod(outcome,8);rouletteTicks=ROULETTE_TOTAL;}
    public static void startSword(int ticks){swordTicks=ticks;}
    public static void tick(){if(deathTicks>0)deathTicks--;if(rouletteTicks>0)rouletteTicks--;if(swordTicks>0)swordTicks--;}
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
    static{for(int i=0;i<8;i++)ROULETTE_ATLAS[i]=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette_"+i+".png");}

    @SubscribeEvent public static void clientSetup(FMLClientSetupEvent e){e.enqueueWork(()->{MenuScreens.register(ModMenus.ATM.get(),AtmScreen::new);MenuScreens.register(ModMenus.SLOT_CONFIG.get(),SlotConfigScreen::new);});}
    @SubscribeEvent public static void registerRenderers(EntityRenderersEvent.RegisterRenderers e){e.registerEntityRenderer(ModEntities.BOSS.get(),ChallengeBossRenderer::new);e.registerBlockEntityRenderer(ModBlockEntities.SLOT_MACHINE.get(),SlotMachineRenderer::new);e.registerBlockEntityRenderer(ModBlockEntities.GRILL.get(),GrillRenderer::new);}
    @SubscribeEvent public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions e){e.registerLayerDefinition(ChallengeBossRenderer.LAYER,com.challengecore.client.render.ChallengeBossModel::createBodyLayer);}

    @Mod.EventBusSubscriber(modid=ChallengeCore.MODID,value=Dist.CLIENT,bus=Mod.EventBusSubscriber.Bus.FORGE)
    public static class ForgeClient {
        private static int lastDeath=0,lastRoulette=0;
        @SubscribeEvent public static void tick(TickEvent.ClientTickEvent e){if(e.phase==TickEvent.Phase.END){ClientState.tick();BossAudioController.tick();}}
        @SubscribeEvent public static void overlay(RenderGuiOverlayEvent.Post e){
            GuiGraphics g=e.getGuiGraphics();int w=g.guiWidth(),h=g.guiHeight();

            if(ClientState.deathTicks>0){
                if(lastDeath==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.DEATH.get(),1f));
                float elapsed=ClientState.DEATH_TOTAL-ClientState.deathTicks;
                float scale=elapsed<15?(.08f+.92f*(elapsed/15f)):1f;
                if(ClientState.deathTicks<28)scale*=.22f+.78f*(ClientState.deathTicks/28f);
                float alpha=ClientState.deathTicks<20?ClientState.deathTicks/20f:1f;

                int size=(int)(Math.min(w,h)*.36f); // smaller, complete and centered
                RenderSystem.enableBlend();RenderSystem.setShaderColor(1,1,1,alpha);
                g.pose().pushPose();g.pose().translate(w/2f,h/2f-18,0);g.pose().scale(scale,scale,1);
                g.blit(DEATH_TEX,-size/2,-size/2,0,0,size,size,512,512);
                g.pose().popPose();RenderSystem.setShaderColor(1,1,1,1);RenderSystem.disableBlend();
                g.drawCenteredString(Minecraft.getInstance().font,ClientState.deadName+" ha muerto",w/2,h/2+size/2-3,0xFFFF3030);
            }
            lastDeath=ClientState.deathTicks;

            if(ClientState.rouletteTicks>0){
                if(lastRoulette==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.ROULETTE_SPIN.get(),1f));
                int rawElapsed=ClientState.ROULETTE_TOTAL-ClientState.rouletteTicks;
                int elapsed=Math.max(0,rawElapsed-ClientState.ROULETTE_VISUAL_DELAY);
                int visualTotal=ClientState.ROULETTE_TOTAL-ClientState.ROULETTE_VISUAL_DELAY;
                int frame=Math.min(141,(elapsed*142)/Math.max(1,visualTotal));
                int col=frame%8,row=frame/8,u=col*256,v=row*256;
                int size=(int)(Math.min(w,h)*.60f);

                float appear=Math.min(1f,elapsed/9f);
                float disappear=Math.min(1f,ClientState.rouletteTicks/11f);
                float sc=Math.min(appear,disappear);
                int draw=Math.max(1,(int)(size*sc)),x=w/2-draw/2,y=h/2-draw/2;
                RenderSystem.enableBlend();
                g.blit(ROULETTE_ATLAS[Math.floorMod(ClientState.rouletteOutcome,8)],x,y,draw,draw,u,v,256,256,2048,4608);
                RenderSystem.disableBlend();
            }
            lastRoulette=ClientState.rouletteTicks;

            if(ClientState.swordTicks>0){RenderSystem.enableBlend();g.blit(SWORD_TEX,0,0,0,0,w,h,512,512);RenderSystem.disableBlend();}
        }
    }
    private ClientEvents(){}
}
''')

# ---------------- Boss: more geometry / relief / animation ----------------
Path("src/main/java/com/challengecore/client/render/ChallengeBossModel.java").write_text(r'''package com.challengecore.client.render;

import com.challengecore.entity.ChallengeBossEntity;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;

public class ChallengeBossModel extends HierarchicalModel<ChallengeBossEntity>{
    private final ModelPart root,torso,head,leftArm,rightArm,leftLeg,rightLeg,sword,backSword,mantle,skirt,maskJaw;

    public ChallengeBossModel(ModelPart root){
        this.root=root;torso=root.getChild("torso");head=root.getChild("head");
        leftArm=root.getChild("left_arm");rightArm=root.getChild("right_arm");leftLeg=root.getChild("left_leg");rightLeg=root.getChild("right_leg");
        sword=rightArm.getChild("sword");backSword=root.getChild("back_sword");mantle=root.getChild("mantle");skirt=root.getChild("skirt");
        maskJaw=head.getChild("mask_jaw");
    }

    public static LayerDefinition createBodyLayer(){
        MeshDefinition m=new MeshDefinition();PartDefinition r=m.getRoot();

        PartDefinition torso=r.addOrReplaceChild("torso",
            CubeListBuilder.create()
                .texOffs(0,32).addBox(-7,-10,-4,14,18,8,new CubeDeformation(.30f))
                .texOffs(48,32).addBox(-8,-8,-5,16,5,10,new CubeDeformation(.32f))
                .texOffs(0,54).addBox(-6,-3,-5,12,12,10,new CubeDeformation(.16f)),
            PartPose.offset(0,5,0));
        torso.addOrReplaceChild("upper_plate",CubeListBuilder.create().texOffs(48,50).addBox(-6,-4,-1,12,7,2,new CubeDeformation(.26f)),PartPose.offset(0,-5,-4.35f));
        torso.addOrReplaceChild("lower_plate",CubeListBuilder.create().texOffs(75,50).addBox(-5,-2,-1,10,6,2,new CubeDeformation(.18f)),PartPose.offset(0,1,-4.42f));
        torso.addOrReplaceChild("belt",CubeListBuilder.create().texOffs(0,76).addBox(-7,-1,-4,14,4,8,new CubeDeformation(.22f)),PartPose.offset(0,7,0));
        torso.addOrReplaceChild("knot",CubeListBuilder.create().texOffs(38,76).addBox(-2,-2,-1,4,4,2,new CubeDeformation(.18f)),PartPose.offset(0,8,-4.7f));

        PartDefinition head=r.addOrReplaceChild("head",
            CubeListBuilder.create()
                .texOffs(0,0).addBox(-5,-6,-5,10,10,10,new CubeDeformation(.10f))
                .texOffs(40,0).addBox(-6,-8,-6,12,5,12,new CubeDeformation(.30f))
                .texOffs(40,20).addBox(-6,-3,-6.4f,12,4,2,new CubeDeformation(.08f)),
            PartPose.offset(0,-9,0));
        head.addOrReplaceChild("brow",CubeListBuilder.create().texOffs(70,18).addBox(-5,-1,-1,10,2,2,new CubeDeformation(.15f)),PartPose.offset(0,-3.2f,-6));
        head.addOrReplaceChild("mask_jaw",CubeListBuilder.create().texOffs(70,24).addBox(-4,-1,-1,8,5,2,new CubeDeformation(.18f)),PartPose.offset(0,.2f,-5.9f));
        head.addOrReplaceChild("fang_l",CubeListBuilder.create().texOffs(94,22).addBox(-1,0,-1,2,5,2),PartPose.offset(3,2,-6.6f));
        head.addOrReplaceChild("fang_r",CubeListBuilder.create().texOffs(94,22).mirror().addBox(-1,0,-1,2,5,2),PartPose.offset(-3,2,-6.6f));
        head.addOrReplaceChild("crest",CubeListBuilder.create().texOffs(82,0).addBox(-1,-13,-1,2,13,2,new CubeDeformation(.12f)),PartPose.offset(0,-5,0));
        head.addOrReplaceChild("crest_tip",CubeListBuilder.create().texOffs(90,0).addBox(-1,-9,-1,2,10,2),PartPose.offsetAndRotation(0,-17,0,0,0,.62f));
        head.addOrReplaceChild("horn_l",CubeListBuilder.create().texOffs(100,0).addBox(0,-1,-1,10,2,2),PartPose.offsetAndRotation(4,-8,0,0,0,-.68f));
        head.addOrReplaceChild("horn_r",CubeListBuilder.create().texOffs(100,0).mirror().addBox(-10,-1,-1,10,2,2),PartPose.offsetAndRotation(-4,-8,0,0,0,.68f));

        PartDefinition la=r.addOrReplaceChild("left_arm",
            CubeListBuilder.create()
                .texOffs(0,92).addBox(0,-3,-3,5,19,6,new CubeDeformation(.16f))
                .texOffs(24,92).addBox(-1,-6,-6,9,7,12,new CubeDeformation(.38f))
                .texOffs(60,92).addBox(0,7,-4,6,8,8,new CubeDeformation(.22f)),
            PartPose.offset(7,-2,0));
        la.addOrReplaceChild("pauldron_top",CubeListBuilder.create().texOffs(88,88).addBox(-1,-2,-5,10,3,10,new CubeDeformation(.14f)),PartPose.offsetAndRotation(3,-6,0,0,0,-.14f));
        la.addOrReplaceChild("pauldron_mid",CubeListBuilder.create().texOffs(88,101).addBox(-1,-1,-5,9,3,10,new CubeDeformation(.12f)),PartPose.offsetAndRotation(4,-3,0,0,0,-.20f));
        la.addOrReplaceChild("spike",CubeListBuilder.create().texOffs(112,88).addBox(0,-1,-1,10,2,2),PartPose.offsetAndRotation(6,-6,0,0,0,-.55f));

        PartDefinition ra=r.addOrReplaceChild("right_arm",
            CubeListBuilder.create()
                .texOffs(0,92).mirror().addBox(-5,-3,-3,5,19,6,new CubeDeformation(.16f))
                .texOffs(24,92).mirror().addBox(-8,-6,-6,9,7,12,new CubeDeformation(.38f))
                .texOffs(60,92).mirror().addBox(-6,7,-4,6,8,8,new CubeDeformation(.22f)),
            PartPose.offset(-7,-2,0));
        ra.addOrReplaceChild("pauldron_top",CubeListBuilder.create().texOffs(88,88).mirror().addBox(-9,-2,-5,10,3,10,new CubeDeformation(.14f)),PartPose.offsetAndRotation(-3,-6,0,0,0,.14f));
        ra.addOrReplaceChild("pauldron_mid",CubeListBuilder.create().texOffs(88,101).mirror().addBox(-8,-1,-5,9,3,10,new CubeDeformation(.12f)),PartPose.offsetAndRotation(-4,-3,0,0,0,.20f));
        ra.addOrReplaceChild("spike",CubeListBuilder.create().texOffs(112,88).mirror().addBox(-10,-1,-1,10,2,2),PartPose.offsetAndRotation(-6,-6,0,0,0,.55f));

        ra.addOrReplaceChild("sword",
            CubeListBuilder.create()
                .texOffs(76,52).addBox(-1,-5,-1,2,30,2)
                .texOffs(88,52).addBox(-2,22,-2,4,13,4)
                .texOffs(104,52).addBox(-8,20,-1,16,2,2),
            PartPose.offsetAndRotation(-2,9,-1,-.18f,0,0));

        r.addOrReplaceChild("back_sword",
            CubeListBuilder.create()
                .texOffs(76,52).addBox(-1,-5,-1,2,34,2)
                .texOffs(88,52).addBox(-2,26,-2,4,14,4)
                .texOffs(104,52).addBox(-8,24,-1,16,2,2),
            PartPose.offsetAndRotation(5,-11,4,-.58f,0,-.76f));

        PartDefinition mantle=r.addOrReplaceChild("mantle",CubeListBuilder.create().texOffs(64,108).addBox(-10,-2,-2,20,5,4,new CubeDeformation(.24f)),PartPose.offset(0,-3,4));
        for(int i=0;i<9;i++)mantle.addOrReplaceChild("feather"+i,CubeListBuilder.create().texOffs(96,108).addBox(-1,-1,0,2,13,2),PartPose.offsetAndRotation(-12+i*3,-1,1,.48f,0,(i-4)*.11f));

        PartDefinition skirt=r.addOrReplaceChild("skirt",CubeListBuilder.create().texOffs(0,112).addBox(-7,-1,-5,14,8,10,new CubeDeformation(.14f)),PartPose.offset(0,12,0));
        skirt.addOrReplaceChild("front_plate",CubeListBuilder.create().texOffs(48,112).addBox(-4,0,-1,8,10,2,new CubeDeformation(.12f)),PartPose.offset(0,1,-5.1f));
        skirt.addOrReplaceChild("left_plate",CubeListBuilder.create().texOffs(70,112).addBox(0,0,-4,2,10,8,new CubeDeformation(.12f)),PartPose.offset(6.8f,1,0));
        skirt.addOrReplaceChild("right_plate",CubeListBuilder.create().texOffs(70,112).mirror().addBox(-2,0,-4,2,10,8,new CubeDeformation(.12f)),PartPose.offset(-6.8f,1,0));

        PartDefinition ll=r.addOrReplaceChild("left_leg",CubeListBuilder.create().texOffs(52,76).addBox(-2,-1,-2,5,17,5,new CubeDeformation(.12f)),PartPose.offset(3,16,0));
        ll.addOrReplaceChild("shin",CubeListBuilder.create().texOffs(104,68).addBox(-3,5,-3,6,10,6,new CubeDeformation(.2f)),PartPose.offset(.5f,0,0));
        PartDefinition rl=r.addOrReplaceChild("right_leg",CubeListBuilder.create().texOffs(52,76).mirror().addBox(-3,-1,-2,5,17,5,new CubeDeformation(.12f)),PartPose.offset(-3,16,0));
        rl.addOrReplaceChild("shin",CubeListBuilder.create().texOffs(104,68).mirror().addBox(-3,5,-3,6,10,6,new CubeDeformation(.2f)),PartPose.offset(-.5f,0,0));

        return LayerDefinition.create(m,128,128);
    }

    @Override public ModelPart root(){return root;}
    @Override public void setupAnim(ChallengeBossEntity e,float limbSwing,float limbAmount,float age,float yaw,float pitch){
        float idle=(float)Math.sin(age*.09f),breathe=(float)Math.sin(age*.13f),weight=(float)Math.sin(age*.055f);
        head.yRot=yaw*((float)Math.PI/180f);head.xRot=pitch*((float)Math.PI/180f)+idle*.025f;
        torso.xScale=1f+breathe*.014f;torso.yScale=1f+breathe*.022f;torso.zScale=1f+breathe*.014f;
        torso.zRot=weight*.012f;mantle.xRot=.04f+idle*.04f;skirt.xRot=idle*.015f;maskJaw.xRot=.03f+breathe*.02f;
        rightArm.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.08f*limbAmount+idle*.04f;
        leftArm.xRot=(float)Math.cos(limbSwing*.6662)*1.08f*limbAmount-idle*.04f;
        rightLeg.xRot=(float)Math.cos(limbSwing*.6662)*1.17f*limbAmount;
        leftLeg.xRot=(float)Math.cos(limbSwing*.6662+Math.PI)*1.17f*limbAmount;
        rightArm.yRot=rightArm.zRot=leftArm.yRot=leftArm.zRot=0;sword.visible=false;backSword.visible=true;
        int state=e.getAttackState();
        if(state==1){float p=(float)Math.sin(age*.82f)*.14f;rightArm.xRot=-1.62f+p;leftArm.xRot=-1.62f-p;rightArm.yRot=-.34f;leftArm.yRot=.34f;torso.xRot=-.10f;}
        else if(state==2){rightArm.xRot=-2.30f;leftArm.xRot=-2.30f;rightArm.zRot=-.53f;leftArm.zRot=.53f;torso.xRot=.10f+(float)Math.sin(age*.4f)*.045f;}
        else if(state==3){sword.visible=true;backSword.visible=false;float stab=(float)Math.sin(age*.95f);rightArm.xRot=-1.88f+stab*.70f;rightArm.yRot=-.30f;leftArm.xRot=-.50f;leftArm.yRot=.20f;torso.yRot=stab*.12f;}
        else {torso.xRot=0;torso.yRot=0;}
        for(int i=0;i<9;i++){ModelPart f=mantle.getChild("feather"+i);f.xRot=.48f+(float)Math.sin(age*.13f+i*.41f)*.075f;}
    }
}
''')

# More faithful large slot cabinet and grill model.
Path("src/main/resources/assets/challengecore/models/block/slot_machine.json").write_text(r'''{
 "parent":"block/block",
 "textures":{"body":"challengecore:block/slot_body","gold":"challengecore:block/slot_gold","reel":"challengecore:block/slot_reel","red":"challengecore:block/slot_red","dark":"challengecore:block/slot_dark","particle":"challengecore:block/slot_body"},
 "elements":[
  {"from":[-2,0,2],"to":[18,9,15],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
  {"from":[-3,8,1],"to":[19,13,15],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#dark"},"down":{"texture":"#body"}}},
  {"from":[-1,13,4],"to":[17,30,15],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#dark"}}},
  {"from":[0,24,2.8],"to":[16,29,4.2],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#gold"},"down":{"texture":"#dark"}}},
  {"from":[.2,15,2.35],"to":[15.8,23.6,4.0],"faces":{"north":{"texture":"#reel"},"south":{"texture":"#dark"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
  {"from":[-1,9.4,.7],"to":[17,13,4],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
  {"from":[8.8,10.0,-.1],"to":[13.8,12.8,1.4],"faces":{"north":{"texture":"#red"},"south":{"texture":"#dark"},"east":{"texture":"#red"},"west":{"texture":"#red"},"up":{"texture":"#red"},"down":{"texture":"#dark"}}},
  {"from":[18.2,11,7],"to":[20,23,10],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#gold"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#gold"},"down":{"texture":"#gold"}}},
  {"from":[19.2,20,7.1],"to":[22.5,23.3,9.9],"faces":{"north":{"texture":"#red"},"south":{"texture":"#red"},"east":{"texture":"#red"},"west":{"texture":"#red"},"up":{"texture":"#red"},"down":{"texture":"#red"}}}
 ],
 "display":{"gui":{"rotation":[30,225,0],"translation":[0,-4,0],"scale":[.5,.5,.5]}}
}''')

Path("src/main/resources/assets/challengecore/models/block/grill.json").write_text(r'''{
 "parent":"block/block",
 "textures":{"metal":"challengecore:block/grill_metal","dark":"challengecore:block/grill_dark","ember":"challengecore:block/grill_ember","particle":"challengecore:block/grill_metal"},
 "elements":[
  {"from":[1,7,1],"to":[15,12,15],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
  {"from":[2,8.5,2],"to":[14,10,14],"faces":{"north":{"texture":"#ember"},"south":{"texture":"#ember"},"east":{"texture":"#ember"},"west":{"texture":"#ember"},"up":{"texture":"#ember"},"down":{"texture":"#dark"}}},
  {"from":[2,11.2,2],"to":[14,11.8,14],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#dark"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
  {"from":[2,0,2],"to":[4,8,4],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#metal"},"down":{"texture":"#metal"}}},
  {"from":[12,0,2],"to":[14,8,4],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#metal"},"down":{"texture":"#metal"}}},
  {"from":[2,0,12],"to":[4,8,14],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#metal"},"down":{"texture":"#metal"}}},
  {"from":[12,0,12],"to":[14,8,14],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#metal"},"down":{"texture":"#metal"}}},
  {"from":[3,3,3],"to":[13,4,13],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
  {"from":[.1,8,6.5],"to":[2,10.5,9.5],"faces":{"north":{"texture":"#metal"},"south":{"texture":"#metal"},"east":{"texture":"#metal"},"west":{"texture":"#metal"},"up":{"texture":"#metal"},"down":{"texture":"#metal"}}}
 ]
}''')
