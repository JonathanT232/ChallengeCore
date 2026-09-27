from pathlib import Path

# version
p=Path("build.gradle")
p.write_text(p.read_text().replace("version = '1.0.0'","version = '1.0.1'"))

# ClientEvents
p=Path("src/main/java/com/challengecore/client/ClientEvents.java")
s=p.read_text()
s=s.replace("import com.challengecore.client.render.ChallengeBossRenderer;","import com.challengecore.client.render.ChallengeBossRenderer;\nimport com.challengecore.client.audio.BossAudioController;")
s=s.replace("import net.minecraftforge.client.event.RegisterMenuScreensEvent;\n","import net.minecraft.client.gui.screens.MenuScreens;\nimport net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;\n")
s=s.replace("@SubscribeEvent public static void registerScreens(RegisterMenuScreensEvent e){e.register(ModMenus.ATM.get(),AtmScreen::new);e.register(ModMenus.SLOT_CONFIG.get(),SlotConfigScreen::new);}",
            "@SubscribeEvent public static void clientSetup(FMLClientSetupEvent e){e.enqueueWork(()->{MenuScreens.register(ModMenus.ATM.get(),AtmScreen::new);MenuScreens.register(ModMenus.SLOT_CONFIG.get(),SlotConfigScreen::new);});}")
s=s.replace('private static final ResourceLocation WHEEL_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette.png");',
            'private static final ResourceLocation WHEEL_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette.png");\n    private static final ResourceLocation POINTER_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette_pointer.png");')
s=s.replace("if(e.phase==TickEvent.Phase.END)ClientState.tick();","if(e.phase==TickEvent.Phase.END){ClientState.tick();BossAudioController.tick();}")
old='''            if(ClientState.rouletteTicks>0){
                if(lastRoulette==0){}
                int size=(int)(Math.min(w,h)*0.55f);float t=140-ClientState.rouletteTicks;float rot=t<90?t*16f:1440f+(t-90)*4f;g.pose().pushPose();g.pose().translate(w/2f,h/2f,0);g.pose().mulPose(Axis.ZP.rotationDegrees(rot));g.blit(WHEEL_TEX,-size/2,-size/2,0,0,size,size,size,size);g.pose().popPose();if(ClientState.rouletteTicks<40){String[] names={"VERDE","AMARILLO","NARANJA","ROJO","ROSA","MORADO","AZUL","CIAN"};g.drawCenteredString(Minecraft.getInstance().font,names[Math.floorMod(ClientState.rouletteOutcome,names.length)],w/2,h/2+size/2+10,0xFFFFFFFF);}
            }'''
new='''            if(ClientState.rouletteTicks>0){
                if(lastRoulette==0)Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.ROULETTE_SPIN.get(),1f));
                int size=(int)(Math.min(w,h)*0.62f);
                float elapsed=180-ClientState.rouletteTicks;
                float progress=Math.min(1f,elapsed/145f);
                float eased=1f-(float)Math.pow(1f-progress,3);
                float target=1440f-(Math.floorMod(ClientState.rouletteOutcome,8)*45f);
                float rot=target*eased;
                float intro=Math.min(1f,elapsed/10f);
                float outro=Math.min(1f,ClientState.rouletteTicks/12f);
                float scale=Math.min(intro,outro);
                RenderSystem.enableBlend();
                g.pose().pushPose();g.pose().translate(w/2f,h/2f,0);g.pose().scale(scale,scale,1);
                g.pose().mulPose(Axis.ZP.rotationDegrees(rot));g.blit(WHEEL_TEX,-size/2,-size/2,0,0,size,size,size,size);
                g.pose().popPose();
                int pw=Math.max(36,size/7),ph=Math.max(42,size/6);
                g.blit(POINTER_TEX,w/2-pw/2,h/2-size/2-ph/3,0,0,pw,ph,pw,ph);
                RenderSystem.disableBlend();
                if(ClientState.rouletteTicks<32){String[] names={"VERDE","AMARILLO","NARANJA","ROJO","ROSA","MORADO","AZUL","CIAN"};g.drawCenteredString(Minecraft.getInstance().font,names[Math.floorMod(ClientState.rouletteOutcome,names.length)],w/2,h/2+size/2+10,0xFFFFFFFF);}
            }'''
if old not in s: raise RuntimeError("roulette block not found")
p.write_text(s.replace(old,new))

p=Path("src/main/java/com/challengecore/client/ClientState.java")
p.write_text(p.read_text().replace("rouletteTicks=140","rouletteTicks=180"))

p=Path("src/main/java/com/challengecore/registry/ModSounds.java")
p.write_text(p.read_text().replace('public static final RegistryObject<SoundEvent> ROULETTE_GREEN = register("roulette_green");',
                                   'public static final RegistryObject<SoundEvent> ROULETTE_GREEN = register("roulette_green");\n    public static final RegistryObject<SoundEvent> ROULETTE_SPIN = register("roulette_spin");'))

Path("src/main/resources/assets/challengecore/sounds.json").write_text("""{
  "death":{"sounds":[{"name":"challengecore:death","stream":true}]},
  "boss_music":{"sounds":[{"name":"challengecore:boss_music","stream":true}]},
  "boss_breath":{"sounds":[{"name":"challengecore:boss_breath","stream":true}]},
  "roulette_green":{"sounds":[{"name":"challengecore:roulette_green","stream":true}]},
  "roulette_spin":{"sounds":[{"name":"challengecore:roulette_spin","stream":true}]},
  "slot_pull":{"sounds":["minecraft:block.lever.click"]},
  "slot_win":{"sounds":["minecraft:entity.player.levelup"]}
}""")

p=Path("src/main/java/com/challengecore/entity/ChallengeBossEntity.java")
p.write_text(p.read_text().replace("Player target=getTarget();","var target=getTarget();").replace("Player t=getTarget();","var t=getTarget();"))

p=Path("src/main/java/com/challengecore/server/ServerEvents.java")
s=p.read_text().replace("if(e.getSource().getEntity() instanceof ChallengeBossEntity boss)boss.discard();",
'''for(ServerLevel sl:dead.getServer().getAllLevels()){
                for(ChallengeBossEntity boss:sl.getEntitiesOfClass(ChallengeBossEntity.class,new net.minecraft.world.phys.AABB(-30000000,-2048,-30000000,30000000,2048,30000000)))boss.discard();
            }''')
p.write_text(s)

for f in ["GrillBlock.java","SlotMachineBlock.java","AtmBlock.java"]:
    p=Path("src/main/java/com/challengecore/block")/f
    s=p.read_text()
    if "import net.minecraft.world.level.block.Block;\n" not in s:
        s=s.replace("import net.minecraft.world.level.block.BaseEntityBlock;\n","import net.minecraft.world.level.block.Block;\nimport net.minecraft.world.level.block.BaseEntityBlock;\n")
    p.write_text(s)

p=Path("src/main/java/com/challengecore/blockentity/SlotMachineBlockEntity.java")
s=p.read_text()
s=s.replace("private final Random random=new Random();","private final Random random=new Random();\n    private int spinTicks=0;")
s=s.replace("for(int i=0;i<3;i++) result[i]=random.nextInt(5);","spinTicks=50;\n        for(int i=0;i<3;i++) result[i]=random.nextInt(5);")
s=s.replace("public int getResult(int i){return result[i];}",'''public int getResult(int i){return result[i];}
    public int getDisplayResult(int i){
        if(spinTicks>0&&level!=null)return Math.floorMod((int)(level.getGameTime()/2L)+i*2,5);
        return result[i];
    }
    public static void tick(net.minecraft.world.level.Level level,net.minecraft.core.BlockPos pos,net.minecraft.world.level.block.state.BlockState state,SlotMachineBlockEntity be){
        if(be.spinTicks>0){be.spinTicks--;if(be.spinTicks==0)be.sync();}
    }''')
s=s.replace('tag.putIntArray("result",result);','tag.putIntArray("result",result); tag.putInt("spinTicks",spinTicks);')
s=s.replace('if(r.length==3)System.arraycopy(r,0,result,0,3); prizes.clear();','if(r.length==3)System.arraycopy(r,0,result,0,3); spinTicks=tag.getInt("spinTicks"); prizes.clear();')
p.write_text(s)

p=Path("src/main/java/com/challengecore/block/SlotMachineBlock.java")
s=p.read_text().replace("import net.minecraft.world.level.block.entity.BlockEntity;","import net.minecraft.world.level.block.entity.BlockEntity;\nimport net.minecraft.world.level.block.entity.BlockEntityTicker;\nimport net.minecraft.world.level.block.entity.BlockEntityType;")
s=s.replace("@Nullable @Override public BlockEntity newBlockEntity(BlockPos p, BlockState s){return new SlotMachineBlockEntity(p,s);}",'''@Nullable @Override public BlockEntity newBlockEntity(BlockPos p, BlockState s){return new SlotMachineBlockEntity(p,s);}
    @Nullable @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type){
        return createTickerHelper(type,com.challengecore.registry.ModBlockEntities.SLOT_MACHINE.get(),SlotMachineBlockEntity::tick);
    }''')
p.write_text(s)

p=Path("src/main/java/com/challengecore/client/render/SlotMachineRenderer.java")
s=p.read_text().replace("be.getResult(i)","be.getDisplayResult(i)")
s=s.replace("pose.translate(.30+i*.20,.92,.02);pose.mulPose(new Quaternionf().rotationX((float)Math.toRadians(90)));pose.scale(.38f,.38f,.38f);",
            "pose.translate(.31+i*.19,.76,.105);pose.mulPose(new Quaternionf().rotationY((float)Math.toRadians(180)));pose.scale(.30f,.30f,.30f);")
p.write_text(s)

p=Path("src/main/java/com/challengecore/blockentity/GrillBlockEntity.java")
p.write_text(p.read_text().replace("public int getFlipCount(){return flipCount;}","public int getFlipCount(){return flipCount;} public int getCookTime(){return cookTime;}"))
p=Path("src/main/java/com/challengecore/client/render/GrillRenderer.java")
p.write_text(p.read_text().replace("float angle=(be.getFlipCount()%2)*180f;pose.mulPose(new Quaternionf().rotationX((float)Math.toRadians(angle)));",
                                   "float angle=be.isCooked()?(be.getFlipCount()%2)*180f:((be.getCookTime()+partial)*2.2f);pose.mulPose(new Quaternionf().rotationX((float)Math.toRadians(angle)));"))

Path("src/main/java/com/challengecore/client/audio/BossLoopSound.java").write_text("""package com.challengecore.client.audio;
import com.challengecore.entity.ChallengeBossEntity;
import net.minecraft.client.resources.sounds.AbstractTickableSoundInstance;
import net.minecraft.client.resources.sounds.SoundInstance;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
public class BossLoopSound extends AbstractTickableSoundInstance {
    private final boolean followBoss; private ChallengeBossEntity boss;
    public BossLoopSound(SoundEvent event,SoundSource source,ChallengeBossEntity boss,boolean followBoss,float volume){
        super(event,source,RandomSource.create());this.boss=boss;this.followBoss=followBoss;this.looping=true;this.delay=0;this.volume=volume;this.pitch=1f;
        this.attenuation=followBoss?SoundInstance.Attenuation.LINEAR:SoundInstance.Attenuation.NONE;
        if(boss!=null){this.x=boss.getX();this.y=boss.getY();this.z=boss.getZ();}
    }
    public void setBoss(ChallengeBossEntity boss){this.boss=boss;}
    @Override public void tick(){if(boss==null||boss.isRemoved()||!boss.isAlive()){stop();return;}if(followBoss){x=boss.getX();y=boss.getY();z=boss.getZ();}}
}
""")

Path("src/main/java/com/challengecore/client/audio/BossAudioController.java").write_text("""package com.challengecore.client.audio;
import com.challengecore.entity.ChallengeBossEntity;
import com.challengecore.registry.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.sounds.SoundSource;
import java.util.List;
public final class BossAudioController {
    private static BossLoopSound music,breath; private static int scanDelay=0;
    public static void tick(){
        Minecraft mc=Minecraft.getInstance();if(mc.level==null||mc.player==null){stop();return;}if(scanDelay-->0)return;scanDelay=5;
        List<ChallengeBossEntity> bosses=mc.level.getEntitiesOfClass(ChallengeBossEntity.class,mc.player.getBoundingBox().inflate(256));
        ChallengeBossEntity boss=bosses.stream().filter(b->b.isAlive()&&!b.isRemoved()).findFirst().orElse(null);
        if(boss==null){stop();return;}
        if(music==null||music.isStopped()){music=new BossLoopSound(ModSounds.BOSS_MUSIC.get(),SoundSource.RECORDS,boss,false,.75f);mc.getSoundManager().play(music);}else music.setBoss(boss);
        if(breath==null||breath.isStopped()){breath=new BossLoopSound(ModSounds.BOSS_BREATH.get(),SoundSource.HOSTILE,boss,true,1f);mc.getSoundManager().play(breath);}else breath.setBoss(boss);
    }
    public static void stop(){if(music!=null){music.stop();music=null;}if(breath!=null){breath.stop();breath=null;}}
    private BossAudioController(){}
}
""")

Path("src/main/resources/assets/challengecore/models/block/speaker.json").write_text("""{
  "parent":"block/block","textures":{"speaker":"challengecore:block/speaker","particle":"challengecore:block/speaker"},
  "elements":[
    {"from":[2,1,4],"to":[14,12,12],"faces":{"north":{"texture":"#speaker"},"south":{"texture":"#speaker"},"east":{"texture":"#speaker"},"west":{"texture":"#speaker"},"up":{"texture":"#speaker"},"down":{"texture":"#speaker"}}},
    {"from":[1.5,2,3.2],"to":[14.5,11.3,4.1],"faces":{"north":{"texture":"#speaker"}}},
    {"from":[3,0,5],"to":[13,1,11],"faces":{"north":{"texture":"#speaker"},"south":{"texture":"#speaker"},"east":{"texture":"#speaker"},"west":{"texture":"#speaker"},"up":{"texture":"#speaker"},"down":{"texture":"#speaker"}}}
  ],"display":{"gui":{"rotation":[30,225,0],"scale":[0.85,0.85,0.85]}}
}""")

Path("src/main/resources/assets/challengecore/models/block/slot_machine.json").write_text("""{
  "parent":"block/block","textures":{"m":"challengecore:block/slot_machine","particle":"challengecore:block/slot_machine"},
  "elements":[
    {"from":[3,0,3],"to":[13,9,13],"faces":{"north":{"texture":"#m"},"south":{"texture":"#m"},"east":{"texture":"#m"},"west":{"texture":"#m"},"up":{"texture":"#m"},"down":{"texture":"#m"}}},
    {"from":[2,8,2],"to":[14,16,13],"faces":{"north":{"texture":"#m"},"south":{"texture":"#m"},"east":{"texture":"#m"},"west":{"texture":"#m"},"up":{"texture":"#m"},"down":{"texture":"#m"}}},
    {"from":[3,10,1.5],"to":[13,15,2.2],"faces":{"north":{"texture":"#m"}}},
    {"from":[14,9,6.5],"to":[15.5,14,8.5],"faces":{"north":{"texture":"#m"},"south":{"texture":"#m"},"east":{"texture":"#m"},"west":{"texture":"#m"},"up":{"texture":"#m"},"down":{"texture":"#m"}}}
  ],"display":{"gui":{"rotation":[30,225,0],"scale":[0.72,0.72,0.72]}}
}""")

Path("src/main/resources/assets/challengecore/models/block/grill.json").write_text("""{
  "parent":"block/block","textures":{"g":"challengecore:block/grill","particle":"challengecore:block/grill"},
  "elements":[
    {"from":[2,6,2],"to":[14,9,14],"faces":{"north":{"texture":"#g"},"south":{"texture":"#g"},"east":{"texture":"#g"},"west":{"texture":"#g"},"up":{"texture":"#g"},"down":{"texture":"#g"}}},
    {"from":[3,9,3],"to":[13,9.8,13],"faces":{"up":{"texture":"#g"}}},
    {"from":[2,0,2],"to":[3,6,3],"faces":{"north":{"texture":"#g"},"south":{"texture":"#g"},"east":{"texture":"#g"},"west":{"texture":"#g"}}},
    {"from":[13,0,2],"to":[14,6,3],"faces":{"north":{"texture":"#g"},"south":{"texture":"#g"},"east":{"texture":"#g"},"west":{"texture":"#g"}}},
    {"from":[2,0,13],"to":[3,6,14],"faces":{"north":{"texture":"#g"},"south":{"texture":"#g"},"east":{"texture":"#g"},"west":{"texture":"#g"}}},
    {"from":[13,0,13],"to":[14,6,14],"faces":{"north":{"texture":"#g"},"south":{"texture":"#g"},"east":{"texture":"#g"},"west":{"texture":"#g"}}}
  ],"display":{"gui":{"rotation":[30,225,0],"scale":[0.8,0.8,0.8]}}
}""")
