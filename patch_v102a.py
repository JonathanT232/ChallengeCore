from pathlib import Path
import json

# Version
p=Path("build.gradle")
s=p.read_text().replace("version = '1.0.1'","version = '1.0.2'").replace("version = '1.0.0'","version = '1.0.2'")
p.write_text(s)

Path("src/main/java/com/challengecore/registry/ModItems.java").write_text(r'''package com.challengecore.registry;

import com.challengecore.ChallengeCore;
import com.challengecore.item.BeerItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModItems {
    public static final DeferredRegister<Item> REGISTER = DeferredRegister.create(ForgeRegistries.ITEMS, ChallengeCore.MODID);

    public static final RegistryObject<Item> BRONZE_COIN = REGISTER.register("bronze_coin", () -> new Item(new Item.Properties().stacksTo(999)));
    public static final RegistryObject<Item> SILVER_COIN = REGISTER.register("silver_coin", () -> new Item(new Item.Properties().stacksTo(999)));
    public static final RegistryObject<Item> GOLD_COIN = REGISTER.register("gold_coin", () -> new Item(new Item.Properties().stacksTo(999)));

    public static final RegistryObject<Item> CASINO_CHIP = REGISTER.register("casino_chip", () -> new Item(new Item.Properties().stacksTo(999)));
    public static final RegistryObject<Item> RED_CHIP = REGISTER.register("red_chip", () -> new Item(new Item.Properties().stacksTo(999)));
    public static final RegistryObject<Item> GOLD_CHIP = REGISTER.register("gold_chip", () -> new Item(new Item.Properties().stacksTo(999)));
    public static final RegistryObject<Item> BLACK_CHIP = REGISTER.register("black_chip", () -> new Item(new Item.Properties().stacksTo(999)));

    public static final RegistryObject<Item> ADMIN_WAND = REGISTER.register("admin_wand", () -> new Item(new Item.Properties().stacksTo(1)));
    public static final RegistryObject<Item> CORONA = REGISTER.register("corona", BeerItem::new);
    public static final RegistryObject<Item> TECATE = REGISTER.register("tecate", BeerItem::new);

    public static final RegistryObject<Item> SYMBOL_RAT = REGISTER.register("symbol_rat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SYMBOL_SEVEN = REGISTER.register("symbol_seven", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SYMBOL_DIAMOND = REGISTER.register("symbol_diamond", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SYMBOL_CHEESE = REGISTER.register("symbol_cheese", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SYMBOL_STAR = REGISTER.register("symbol_star", () -> new Item(new Item.Properties()));

    public static RegistryObject<Item> blockItem(String name, RegistryObject<? extends net.minecraft.world.level.block.Block> block) {
        return REGISTER.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
    }
    private ModItems() {}
}
''')

Path("src/main/java/com/challengecore/blockentity/AtmBlockEntity.java").write_text(r'''package com.challengecore.blockentity;

import com.challengecore.menu.AtmMenu;
import com.challengecore.registry.ModBlockEntities;
import com.challengecore.registry.ModItems;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.common.capabilities.Capability;
import net.minecraftforge.common.capabilities.ForgeCapabilities;
import net.minecraftforge.common.util.LazyOptional;
import net.minecraftforge.items.ItemStackHandler;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class AtmBlockEntity extends BlockEntity implements MenuProvider {
    private boolean exchanging=false;
    private final ItemStackHandler items=new ItemStackHandler(2){
        @Override protected void onContentsChanged(int slot){setChanged();if(slot==0)exchange();}
        @Override public boolean isItemValid(int slot,@NotNull ItemStack stack){
            return slot==0&&(stack.is(ModItems.BRONZE_COIN.get())||stack.is(ModItems.SILVER_COIN.get())||stack.is(ModItems.GOLD_COIN.get()));
        }
        @Override public int getSlotLimit(int slot){return 999;}
    };
    private LazyOptional<ItemStackHandler> lazy=LazyOptional.of(()->items);
    public AtmBlockEntity(BlockPos p,BlockState s){super(ModBlockEntities.ATM.get(),p,s);}

    private void exchange(){
        if(exchanging)return;
        exchanging=true;
        ItemStack in=items.getStackInSlot(0);
        Item chip=null;
        int amount=0;
        if(in.is(ModItems.BRONZE_COIN.get())){chip=ModItems.RED_CHIP.get();amount=1;}
        else if(in.is(ModItems.SILVER_COIN.get())){chip=ModItems.GOLD_CHIP.get();amount=10;}
        else if(in.is(ModItems.GOLD_COIN.get())){chip=ModItems.BLACK_CHIP.get();amount=100;}

        if(chip!=null){
            ItemStack out=items.getStackInSlot(1);
            int limit=chip.getMaxStackSize();
            int room=out.isEmpty()?limit:out.is(chip)?limit-out.getCount():0;
            if(room>=amount){
                in.shrink(1);
                if(out.isEmpty())items.setStackInSlot(1,new ItemStack(chip,amount));else out.grow(amount);
            }
        }
        exchanging=false;
    }

    public ItemStackHandler getItems(){return items;}
    @Override protected void saveAdditional(CompoundTag tag){super.saveAdditional(tag);tag.put("inv",items.serializeNBT());}
    @Override public void load(CompoundTag tag){super.load(tag);items.deserializeNBT(tag.getCompound("inv"));}
    @Override public Component getDisplayName(){return Component.translatable("block.challengecore.atm");}
    @Nullable @Override public AbstractContainerMenu createMenu(int id,Inventory inv,Player p){return new AtmMenu(id,inv,this);}
    @Override public <T> LazyOptional<T> getCapability(@NotNull Capability<T> cap,@Nullable Direction side){return cap==ForgeCapabilities.ITEM_HANDLER?lazy.cast():super.getCapability(cap,side);}
    @Override public void invalidateCaps(){super.invalidateCaps();lazy.invalidate();}
}
''')

Path("src/main/java/com/challengecore/menu/AtmMenu.java").write_text(r'''package com.challengecore.menu;

import com.challengecore.blockentity.AtmBlockEntity;
import com.challengecore.registry.ModBlocks;
import com.challengecore.registry.ModMenus;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.items.SlotItemHandler;

public class AtmMenu extends AbstractContainerMenu {
    private final AtmBlockEntity be;
    public AtmMenu(int id,Inventory inv,FriendlyByteBuf buf){this(id,inv,(AtmBlockEntity)inv.player.level().getBlockEntity(buf.readBlockPos()));}
    public AtmMenu(int id,Inventory inv,AtmBlockEntity be){
        super(ModMenus.ATM.get(),id);this.be=be;
        addSlot(new SlotItemHandler(be.getItems(),0,73,57));
        addSlot(new SlotItemHandler(be.getItems(),1,165,57){@Override public boolean mayPlace(ItemStack s){return false;}});
        addPlayer(inv);
    }
    private void addPlayer(Inventory inv){
        for(int r=0;r<3;r++)for(int c=0;c<9;c++)addSlot(new Slot(inv,c+r*9+9,47+c*18,124+r*18));
        for(int c=0;c<9;c++)addSlot(new Slot(inv,c,47+c*18,182));
    }
    @Override public ItemStack quickMoveStack(Player p,int index){
        ItemStack ret=ItemStack.EMPTY;Slot slot=slots.get(index);
        if(slot!=null&&slot.hasItem()){
            ItemStack s=slot.getItem();ret=s.copy();
            if(index<2){if(!moveItemStackTo(s,2,38,true))return ItemStack.EMPTY;}
            else if(!moveItemStackTo(s,0,1,false))return ItemStack.EMPTY;
            if(s.isEmpty())slot.set(ItemStack.EMPTY);else slot.setChanged();
        }
        return ret;
    }
    @Override public boolean stillValid(Player p){return stillValid(net.minecraft.world.inventory.ContainerLevelAccess.create(be.getLevel(),be.getBlockPos()),p,ModBlocks.ATM.get());}
}
''')

Path("src/main/java/com/challengecore/client/screen/AtmScreen.java").write_text(r'''package com.challengecore.client.screen;

import com.challengecore.menu.AtmMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;

public class AtmScreen extends AbstractContainerScreen<AtmMenu> {
    public AtmScreen(AtmMenu menu,Inventory inv,Component title){
        super(menu,inv,title);imageWidth=256;imageHeight=220;inventoryLabelY=111;inventoryLabelX=47;titleLabelX=10;titleLabelY=8;
    }
    @Override protected void renderBg(GuiGraphics g,float pt,int mx,int my){
        int x=(width-imageWidth)/2,y=(height-imageHeight)/2;
        g.fill(x,y,x+imageWidth,y+imageHeight,0xF0181C22);
        g.fill(x+4,y+4,x+imageWidth-4,y+imageHeight-4,0xFF2D333B);
        g.fill(x+10,y+24,x+imageWidth-10,y+104,0xFF101419);
        g.fill(x+16,y+30,x+imageWidth-16,y+98,0xFF18252A);
        g.drawCenteredString(font,"CAJERO CHALLENGE",x+imageWidth/2,y+12,0xFFFFFFFF);
        g.drawString(font,"INSERTA MONEDA",x+43,y+40,0xFFBDE8E1,false);
        g.drawString(font,"RECIBE FICHAS",x+145,y+40,0xFFBDE8E1,false);
        g.fill(x+69,y+53,x+95,y+79,0xFF313B47);
        g.fill(x+161,y+53,x+187,y+79,0xFF313B47);
        g.drawCenteredString(font,"BRONCE $1  ->  1 FICHA ROJA",x+imageWidth/2,y+82,0xFFFF5656);
        g.drawCenteredString(font,"PLATA $10  ->  10 FICHAS DORADAS",x+imageWidth/2,y+92,0xFFFFD54A);
        g.drawCenteredString(font,"ORO $100  ->  100 FICHAS NEGRAS",x+imageWidth/2,y+102,0xFFE7E7E7);
        g.fill(x+38,y+116,x+218,y+210,0xCC171A20);
    }
    @Override protected void renderLabels(GuiGraphics g,int mx,int my){
        g.drawString(font,title,titleLabelX,titleLabelY,0xFFEAEAEA,false);
        g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xFFBFC5CC,false);
    }
    @Override public void render(GuiGraphics g,int mx,int my,float pt){renderBackground(g);super.render(g,mx,my,pt);renderTooltip(g,mx,my);}
}
''')

# Creative tab entries
p=Path("src/main/java/com/challengecore/ChallengeCore.java")
s=p.read_text()
s=s.replace("e.accept(ModItems.CASINO_CHIP.get());\n            e.accept(ModItems.ADMIN_WAND.get());",
'''e.accept(ModItems.RED_CHIP.get());
            e.accept(ModItems.GOLD_CHIP.get());
            e.accept(ModItems.BLACK_CHIP.get());
            e.accept(ModItems.ADMIN_WAND.get());''')
p.write_text(s)

# Lang + item models
p=Path("src/main/resources/assets/challengecore/lang/es_mx.json")
j=json.loads(p.read_text())
j["item.challengecore.red_chip"]="Ficha Roja"
j["item.challengecore.gold_chip"]="Ficha Dorada"
j["item.challengecore.black_chip"]="Ficha Negra"
p.write_text(json.dumps(j,ensure_ascii=False,indent=2))

for name in ("red_chip","gold_chip","black_chip"):
    Path(f"src/main/resources/assets/challengecore/models/item/{name}.json").write_text(json.dumps({
        "parent":"minecraft:item/generated","textures":{"layer0":f"challengecore:item/{name}"}
    }))

# Casino accepts all chip colors; sensible default prizes
p=Path("src/main/java/com/challengecore/block/SlotMachineBlock.java")
s=p.read_text().replace("held.is(ModItems.CASINO_CHIP.get())",
"(held.is(ModItems.RED_CHIP.get())||held.is(ModItems.GOLD_CHIP.get())||held.is(ModItems.BLACK_CHIP.get())||held.is(ModItems.CASINO_CHIP.get()))")
p.write_text(s)

p=Path("src/main/java/com/challengecore/blockentity/SlotMachineBlockEntity.java")
s=p.read_text()
s=s.replace("if(key==rat) return new ItemStack(ModItems.CASINO_CHIP.get(),64);","if(key==rat) return new ItemStack(ModItems.BLACK_CHIP.get(),1);")
s=s.replace("if(a==b&&b==c) return new ItemStack(ModItems.CASINO_CHIP.get(),20);","if(a==b&&b==c) return new ItemStack(ModItems.GOLD_CHIP.get(),2);")
s=s.replace("if(a==b||a==c||b==c) return new ItemStack(ModItems.CASINO_CHIP.get(),4);","if(a==b||a==c||b==c) return new ItemStack(ModItems.RED_CHIP.get(),4);")
p.write_text(s)

Path("src/main/resources/assets/challengecore/models/block/slot_machine.json").write_text(r'''{
  "parent":"block/block",
  "textures":{"body":"challengecore:block/slot_body","gold":"challengecore:block/slot_gold","reel":"challengecore:block/slot_reel","particle":"challengecore:block/slot_body"},
  "elements":[
    {"from":[2,0,3],"to":[14,5,14],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#body"}}},
    {"from":[1.5,5,2.5],"to":[14.5,8,14],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[2,8,4],"to":[14,16,14],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[2,14,3.2],"to":[14,16,4.2],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[2.6,9,3],"to":[13.4,14,3.8],"faces":{"north":{"texture":"#reel"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#body"}}},
    {"from":[9,5.8,1.8],"to":[12,7,3],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[14,7,7],"to":[15,13,9],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#gold"},"west":{"texture":"#body"},"up":{"texture":"#gold"},"down":{"texture":"#body"}}},
    {"from":[15,11.5,7.3],"to":[16,13.5,8.7],"faces":{"north":{"texture":"#gold"},"south":{"texture":"#gold"},"east":{"texture":"#gold"},"west":{"texture":"#gold"},"up":{"texture":"#gold"},"down":{"texture":"#gold"}}}
  ],
  "display":{"gui":{"rotation":[30,225,0],"scale":[0.78,0.78,0.78]}}
}''')

Path("src/main/resources/assets/challengecore/models/block/atm.json").write_text(r'''{
  "parent":"block/block",
  "textures":{"body":"challengecore:block/atm_body","dark":"challengecore:block/atm_dark","screen":"challengecore:block/atm_screen","particle":"challengecore:block/atm_body"},
  "elements":[
    {"from":[2,0,3],"to":[14,16,14],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[2.4,9,2],"to":[13.6,15,4],"rotation":{"origin":[8,9,4],"axis":"x","angle":-22.5},"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[3.3,10.1,1.45],"to":[12.7,14.2,2.05],"rotation":{"origin":[8,9,4],"axis":"x","angle":-22.5},"faces":{"north":{"texture":"#screen"},"south":{"texture":"#dark"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
    {"from":[3,5.8,1.9],"to":[10.2,8,3],"faces":{"north":{"texture":"#body"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[4,6.3,1.35],"to":[9.2,7.2,2],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#dark"},"east":{"texture":"#dark"},"west":{"texture":"#dark"},"up":{"texture":"#dark"},"down":{"texture":"#dark"}}},
    {"from":[10.8,5.6,2],"to":[13.2,8.3,4],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}},
    {"from":[4,2.8,1.6],"to":[11,4.4,2.4],"faces":{"north":{"texture":"#dark"},"south":{"texture":"#body"},"east":{"texture":"#body"},"west":{"texture":"#body"},"up":{"texture":"#body"},"down":{"texture":"#dark"}}}
  ],
  "display":{"gui":{"rotation":[30,225,0],"scale":[0.75,0.75,0.75]}}
}''')
