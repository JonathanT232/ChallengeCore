from pathlib import Path

# version
p=Path('build.gradle'); s=p.read_text();
import re
s=re.sub(r"version = '[^']+'","version = '1.0.8'",s,count=1); p.write_text(s)

Path('src/main/java/com/challengecore/client/ClientState.java').write_text(r'''package com.challengecore.client;
public final class ClientState {
    public static final int DEATH_TOTAL=160;
    public static int deathTicks=0,swordTicks=0,rouletteOutcome=0;
    public static String deadName="";
    public static boolean rouletteActive=false;
    public static long rouletteStartMs=0L;
    public static final long ROULETTE_DURATION_MS=7235L;
    public static float rouletteStartAngle=0f,rouletteTargetAngle=0f;
    public static void startDeath(String name){deadName=name;deathTicks=DEATH_TOTAL;}
    public static void startRoulette(int outcome){
        rouletteOutcome=Math.floorMod(outcome,8);
        rouletteStartMs=System.currentTimeMillis();
        rouletteStartAngle=0f;
        rouletteTargetAngle=360f*7f-(rouletteOutcome*45f);
        rouletteActive=true;
    }
    public static void startSword(int ticks){swordTicks=ticks;}
    public static void tick(){
        if(deathTicks>0)deathTicks--;
        if(swordTicks>0)swordTicks--;
        if(rouletteActive && System.currentTimeMillis()-rouletteStartMs>=ROULETTE_DURATION_MS+700L) rouletteActive=false;
    }
    private ClientState(){}
}
''')

Path('src/main/java/com/challengecore/client/ClientEvents.java').write_text(r'''package com.challengecore.client;

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
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.MenuScreens;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
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
    private static final ResourceLocation WHEEL_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette_wheel.png");
    private static final ResourceLocation POINTER_TEX=new ResourceLocation(ChallengeCore.MODID,"textures/gui/roulette_pointer_v108.png");
    @SubscribeEvent public static void clientSetup(FMLClientSetupEvent e){e.enqueueWork(()->{MenuScreens.register(ModMenus.ATM.get(),AtmScreen::new);MenuScreens.register(ModMenus.SLOT_CONFIG.get(),SlotConfigScreen::new);});}
    @SubscribeEvent public static void registerRenderers(EntityRenderersEvent.RegisterRenderers e){e.registerEntityRenderer(ModEntities.BOSS.get(),ChallengeBossRenderer::new);e.registerBlockEntityRenderer(ModBlockEntities.SLOT_MACHINE.get(),SlotMachineRenderer::new);e.registerBlockEntityRenderer(ModBlockEntities.GRILL.get(),GrillRenderer::new);}
    @SubscribeEvent public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions e){e.registerLayerDefinition(ChallengeBossRenderer.LAYER,com.challengecore.client.render.ChallengeBossModel::createBodyLayer);}

    @Mod.EventBusSubscriber(modid=ChallengeCore.MODID,value=Dist.CLIENT,bus=Mod.EventBusSubscriber.Bus.FORGE)
    public static class ForgeClient {
        private static boolean rouletteSoundStarted=false;
        private static int lastDeath=0;
        @SubscribeEvent public static void tick(TickEvent.ClientTickEvent e){if(e.phase==TickEvent.Phase.END){ClientState.tick();BossAudioController.tick();}}
        @SubscribeEvent public static void overlay(RenderGuiOverlayEvent.Post e){
            GuiGraphics g=e.getGuiGraphics(); int w=g.guiWidth(),h=g.guiHeight();
            if(ClientState.deathTicks>0){
                if(lastDeath==0) Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.DEATH.get(),1f));
                float elapsed=ClientState.DEATH_TOTAL-ClientState.deathTicks;
                float sc=elapsed<16f?Mth.clamp(elapsed/16f,.08f,1f):1f;
                if(ClientState.deathTicks<28) sc*=Mth.clamp(ClientState.deathTicks/28f,.08f,1f);
                int draw=Math.min(220,(int)(Math.min(w,h)*.29f));
                int cx=w/2,cy=h/2+35;
                RenderSystem.enableBlend();
                g.pose().pushPose();g.pose().translate(cx,cy,0);g.pose().scale(sc,sc,1);
                g.blit(DEATH_TEX,-draw/2,-draw/2,0,0,draw,draw,512,512);
                g.pose().popPose();RenderSystem.disableBlend();
                g.drawCenteredString(Minecraft.getInstance().font,ClientState.deadName+" ha muerto",cx,cy+draw/2+5,0xFFFF3030);
            }
            lastDeath=ClientState.deathTicks;

            if(ClientState.rouletteActive){
                if(!rouletteSoundStarted){Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(ModSounds.ROULETTE_SPIN.get(),1f));rouletteSoundStarted=true;}
                long elapsedMs=System.currentTimeMillis()-ClientState.rouletteStartMs;
                float p=Mth.clamp(elapsedMs/(float)ClientState.ROULETTE_DURATION_MS,0f,1f);
                float eased=1f-(float)Math.pow(1f-p,5.0);
                float rot=Mth.lerp(eased,ClientState.rouletteStartAngle,ClientState.rouletteTargetAngle);
                int size=(int)(Math.min(w,h)*.61f);
                float intro=Mth.clamp(p/.055f,0f,1f);
                float outro=p>.96f?Mth.clamp((1f-p)/.04f,0f,1f):1f;
                float sc=Math.min(intro,outro);
                RenderSystem.enableBlend();
                g.pose().pushPose();g.pose().translate(w/2f,h/2f,0);g.pose().scale(sc,sc,1);g.pose().mulPose(Axis.ZP.rotationDegrees(rot));
                g.blit(WHEEL_TEX,-size/2,-size/2,0,0,size,size,512,512);
                g.pose().popPose();
                int pw=Math.max(58,size/6),ph=pw;
                g.blit(POINTER_TEX,w/2-pw/2,h/2-size/2-ph/3,0,0,pw,ph,180,180);
                RenderSystem.disableBlend();
                if(p>.91f){String[] n={"VERDE","AMARILLO","NARANJA","ROJO","ROSA","MORADO","AZUL","CIAN"};g.drawCenteredString(Minecraft.getInstance().font,n[ClientState.rouletteOutcome],w/2,h/2+size/2+10,0xFFFFFFFF);}
            }else rouletteSoundStarted=false;
        }
    }
    private ClientEvents(){}
}
''')

# Boss damage/rapid sword combo: keep current detailed v105 model, fix combat numbers.
p=Path('src/main/java/com/challengecore/entity/ChallengeBossEntity.java'); s=p.read_text()
s=s.replace('.add(Attributes.ATTACK_DAMAGE,12.0)','.add(Attributes.ATTACK_DAMAGE,1.0)')
s=s.replace('swordHits=9;swordDelay=1;', 'swordHits=26;swordDelay=1;')
s=s.replace('swordDelay=10;', 'swordDelay=2;')
s=re.sub(r'float dmg=swordHits==1\?2f:6f;[^\n]*\n\s*t\.hurt\(level\(\)\.damageSources\(\)\.mobAttack\(this\),dmg\);', 'float dmg=1.0f;\n        t.hurt(level().damageSources().mobAttack(this),dmg);', s)
s=s.replace('new BossSwordOverlayPacket(180)','new BossSwordOverlayPacket(70)')
p.write_text(s)

Path('GenerateAssets108.java').write_text(r'''import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;
public class GenerateAssets108 {
  static final Color[] C={new Color(20,207,65),new Color(255,215,31),new Color(255,150,19),new Color(255,68,74),new Color(255,69,193),new Color(145,72,231),new Color(56,89,233),new Color(39,196,213)};
  static void ensure(File f){f.mkdirs();}
  static void write(BufferedImage i,String p)throws Exception{File f=new File(p);ensure(f.getParentFile());ImageIO.write(i,"png",f);}
  static void wheel()throws Exception{
    int n=512,c=n/2,r=214; BufferedImage im=new BufferedImage(n,n,BufferedImage.TYPE_INT_ARGB);Graphics2D g=im.createGraphics();g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
    for(int i=0;i<8;i++){double center=-90+i*45;double start=center-22.5;g.setColor(C[i]);g.fill(new Arc2D.Double(c-r,c-r,r*2,r*2,-start,-45,Arc2D.PIE));}
    g.setStroke(new BasicStroke(12));g.setColor(new Color(15,15,17));g.drawOval(c-r,c-r,r*2,r*2);
    for(int i=0;i<8;i++){double a=Math.toRadians(-90+22.5+i*45);int x=(int)(c+r*Math.cos(a)),y=(int)(c+r*Math.sin(a));g.drawLine(c,c,x,y);}
    g.setColor(new Color(247,174,17));g.setStroke(new BasicStroke(6));g.drawOval(c-r-8,c-r-8,r*2+16,r*2+16);
    g.setColor(new Color(255,255,255,90));g.setStroke(new BasicStroke(10));g.drawArc(c-r+22,c-r+22,(r-22)*2,(r-22)*2,25,110);
    for(int i=0;i<8;i++){double a=Math.toRadians(-90+i*45);int x=(int)(c+155*Math.cos(a)),y=(int)(c+155*Math.sin(a));g.setColor(new Color(255,255,255,220));g.fillOval(x-6,y-6,12,12);}
    g.setColor(new Color(12,12,14));g.fillOval(c-50,c-50,100,100);g.setColor(new Color(246,181,9));g.fillOval(c-39,c-39,78,78);g.setColor(new Color(255,232,104));g.fillOval(c-23,c-23,46,46);g.dispose();write(im,"src/main/resources/assets/challengecore/textures/gui/roulette_wheel.png");
  }
  static void pointer()throws Exception{BufferedImage im=new BufferedImage(180,180,BufferedImage.TYPE_INT_ARGB);Graphics2D g=im.createGraphics();g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);Path2D p=new Path2D.Double();p.moveTo(90,15);p.lineTo(145,62);p.lineTo(113,70);p.lineTo(103,162);p.lineTo(77,162);p.lineTo(67,70);p.lineTo(35,62);p.closePath();g.setStroke(new BasicStroke(7));g.setColor(new Color(15,15,17));g.draw(p);g.setPaint(new GradientPaint(0,0,new Color(255,224,87),180,180,new Color(242,137,0)));g.fill(p);g.setColor(new Color(15,15,17));g.draw(p);g.dispose();write(im,"src/main/resources/assets/challengecore/textures/gui/roulette_pointer_v108.png");}
  static void simple(String path,Color a,Color b)throws Exception{BufferedImage im=new BufferedImage(64,64,BufferedImage.TYPE_INT_ARGB);Graphics2D g=im.createGraphics();g.setPaint(new GradientPaint(0,0,a,64,64,b));g.fillRect(0,0,64,64);g.setColor(new Color(255,255,255,50));for(int y=4;y<64;y+=8)g.drawLine(0,y,64,y);g.setColor(new Color(0,0,0,130));g.drawRect(1,1,61,61);g.dispose();write(im,path);}
  public static void main(String[]x)throws Exception{wheel();pointer();String r="src/main/resources/assets/challengecore/textures/block/";simple(r+"atm_body.png",new Color(185,191,198),new Color(65,72,80));simple(r+"atm_dark.png",new Color(38,42,46),new Color(7,9,11));simple(r+"atm_screen.png",new Color(26,98,96),new Color(3,22,25));simple(r+"speaker.png",new Color(28,31,34),new Color(3,4,5));}
}
''')
