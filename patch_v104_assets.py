from pathlib import Path

Path("GenerateAssets104.java").write_text(r'''import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Random;

public class GenerateAssets104 {
  static final Color[] COLORS={
    new Color(20,207,65), new Color(255,215,31), new Color(255,150,19), new Color(255,68,74),
    new Color(255,69,193), new Color(145,72,231), new Color(56,89,233), new Color(39,196,213)
  };

  static BufferedImage baseWheel(double angle, int outcome, double recolor, double flash){
    int n=256,c=n/2,r=104;
    BufferedImage img=new BufferedImage(n,n,BufferedImage.TYPE_INT_ARGB);
    Graphics2D g=img.createGraphics();
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
    g.translate(c,c);
    g.rotate(Math.toRadians(angle));
    g.translate(-c,-c);

    for(int i=0;i<8;i++){
      Color a=COLORS[i],b=COLORS[outcome];
      int rr=(int)(a.getRed()*(1-recolor)+b.getRed()*recolor);
      int gg=(int)(a.getGreen()*(1-recolor)+b.getGreen()*recolor);
      int bb=(int)(a.getBlue()*(1-recolor)+b.getBlue()*recolor);
      g.setColor(new Color(rr,gg,bb));
      g.fill(new Arc2D.Double(c-r,c-r,r*2,r*2,90-i*45,-45,Arc2D.PIE));
    }
    g.setStroke(new BasicStroke(7f,BasicStroke.CAP_ROUND,BasicStroke.JOIN_ROUND));
    g.setColor(new Color(16,16,19));
    g.drawOval(c-r,c-r,r*2,r*2);
    for(int i=0;i<8;i++){
      double a=Math.toRadians(90-i*45);
      g.drawLine(c,c,(int)(c+r*Math.cos(a)),(int)(c-r*Math.sin(a)));
    }
    g.setStroke(new BasicStroke(3f));g.setColor(new Color(255,181,12));
    g.drawOval(c-r-3,c-r-3,r*2+6,r*2+6);
    g.setStroke(new BasicStroke(7f));g.setColor(new Color(255,255,255,72));
    g.drawArc(c-r+10,c-r+10,(r-10)*2,(r-10)*2,20,128);

    int[][] pts={{63,72},{84,56},{190,72},{206,112},{194,174},{167,204},{84,198},{55,153}};
    g.setColor(new Color(255,255,255,210));
    for(int[] p:pts)g.fillOval(p[0]-3,p[1]-3,6,6);

    g.setColor(new Color(14,14,18));g.fillOval(c-23,c-23,46,46);
    g.setColor(new Color(249,185,8));g.fillOval(c-18,c-18,36,36);
    g.setColor(new Color(255,229,90));g.fillOval(c-11,c-11,22,22);

    g.translate(c,c);g.rotate(Math.toRadians(-angle));g.translate(-c,-c);

    // Fixed Dedsafio-like pointer at upper-left, never rotates.
    Path2D p=new Path2D.Double();
    p.moveTo(13,70);p.lineTo(53,54);p.lineTo(74,68);p.lineTo(67,102);p.lineTo(17,98);p.closePath();
    g.setStroke(new BasicStroke(5f,BasicStroke.JOIN_ROUND,BasicStroke.CAP_ROUND));
    g.setColor(new Color(14,14,18));g.draw(p);
    g.setPaint(new GradientPaint(15,62,new Color(255,196,20),72,100,new Color(245,126,0)));g.fill(p);
    g.setColor(new Color(14,14,18));g.draw(p);
    g.setColor(new Color(15,15,18));g.fillOval(31,65,30,30);
    for(int i=0;i<6;i++){g.setColor(COLORS[(i+1)%8]);g.fill(new Arc2D.Double(35,69,22,22,90-i*60,-60,Arc2D.PIE));}
    g.setColor(new Color(255,220,35));g.fillOval(42,76,8,8);

    if(flash>0){
      int a=(int)(Math.min(1,flash)*255);
      g.setColor(new Color(255,255,255,a));
      g.fillOval(c-r-8,c-r-8,r*2+16,r*2+16);
    }

    g.dispose();return img;
  }

  static double smooth(double t){t=Math.max(0,Math.min(1,t));return 1-Math.pow(1-t,4);}

  static void makeRouletteAtlases() throws Exception{
    File gui=new File("src/main/resources/assets/challengecore/textures/gui");gui.mkdirs();
    for(int outcome=0;outcome<8;outcome++){
      BufferedImage atlas=new BufferedImage(2048,4608,BufferedImage.TYPE_INT_ARGB);
      Graphics2D ag=atlas.createGraphics();
      for(int frame=0;frame<142;frame++){
        double angle,recolor=0,flash=0;
        if(frame<=109){
          double t=frame/109.0;
          double target=360*7 + (outcome*45.0);
          angle=target*smooth(t);
        }else{
          angle=360*7 + outcome*45.0;
          if(frame<=130)recolor=(frame-109)/21.0;
          else recolor=1;
          if(frame>=137)flash=(frame-136)/5.0;
        }
        BufferedImage fr=baseWheel(angle,outcome,recolor,flash);
        ag.drawImage(fr,(frame%8)*256,(frame/8)*256,null);
      }
      ag.dispose();
      ImageIO.write(atlas,"png",new File(gui,"roulette_"+outcome+".png"));
    }
  }

  static void makeBossTexture() throws Exception{
    File ent=new File("src/main/resources/assets/challengecore/textures/entity");ent.mkdirs();
    BufferedImage img=new BufferedImage(128,128,BufferedImage.TYPE_INT_ARGB);
    Graphics2D g=img.createGraphics();
    g.setColor(new Color(9,10,12));g.fillRect(0,0,128,128);

    // Rich black/charcoal base with pixel variation.
    Random rnd=new Random(232);
    for(int y=0;y<128;y+=4)for(int x=0;x<128;x+=4){
      int v=14+rnd.nextInt(24);
      g.setColor(new Color(v,v+1,v+2));g.fillRect(x,y,4,4);
    }

    // Gold/orange lacquer plates and highlights across all UV regions.
    g.setColor(new Color(75,44,13));
    for(int y=0;y<128;y+=16)g.fillRect(0,y,128,3);
    g.setColor(new Color(202,111,7));
    for(int y=5;y<128;y+=17)g.fillRect(0,y,128,4);
    g.setColor(new Color(246,168,22));
    for(int x=7;x<128;x+=23)g.fillRect(x,0,4,128);
    g.setColor(new Color(255,205,62));
    for(int x=4;x<124;x+=24){g.fillRect(x,3,10,3);g.fillRect(x,29,9,3);g.fillRect(x,61,12,3);}

    // Helmet, face, mask zones.
    g.setColor(new Color(37,28,22));g.fillRect(0,0,32,22);
    g.setColor(new Color(190,122,47));g.fillRect(6,5,20,12);
    g.setColor(new Color(229,176,92));g.fillRect(9,7,14,8);
    g.setColor(new Color(9,10,12));g.fillRect(11,9,4,3);g.fillRect(19,9,4,3);
    g.setColor(new Color(132,70,10));g.fillRect(40,0,39,17);
    g.setColor(new Color(249,181,28));g.fillRect(42,2,35,4);

    // Chest armor / sash.
    g.setColor(new Color(28,29,32));g.fillRect(0,32,46,22);
    g.setColor(new Color(232,138,12));g.fillRect(3,35,40,5);
    g.setColor(new Color(245,185,33));g.fillRect(5,43,36,3);
    g.setColor(new Color(80,36,10));g.fillRect(48,32,37,18);
    g.setColor(new Color(245,174,20));g.fillRect(51,34,31,4);
    g.setColor(new Color(48,49,53));g.fillRect(51,41,31,6);

    // Arm/gauntlet metal zones.
    g.setColor(new Color(71,73,78));g.fillRect(0,92,22,25);g.fillRect(24,92,34,25);
    g.setColor(new Color(226,139,16));g.fillRect(2,94,18,4);g.fillRect(27,94,28,4);
    g.setColor(new Color(247,191,47));g.fillRect(2,105,18,3);g.fillRect(27,105,28,3);

    // Skirt plates and cloth.
    g.setColor(new Color(17,18,21));g.fillRect(0,112,90,16);
    g.setColor(new Color(205,106,5));g.fillRect(0,114,90,4);
    g.setColor(new Color(240,167,23));g.fillRect(4,121,82,3);

    // Sword steel + gold hilt.
    g.setColor(new Color(156,161,168));g.fillRect(76,52,10,36);
    g.setColor(new Color(226,228,232));g.fillRect(78,54,4,32);
    g.setColor(new Color(244,172,27));g.fillRect(88,52,17,20);
    g.setColor(new Color(113,57,7));g.fillRect(91,54,4,18);

    // Small bright rivets.
    g.setColor(new Color(255,219,96));
    for(int y=6;y<122;y+=18)for(int x=6;x<124;x+=29)g.fillRect(x,y,2,2);

    g.dispose();
    ImageIO.write(img,"png",new File(ent,"crimson_boss.png"));
  }

  public static void main(String[] args)throws Exception{
    makeRouletteAtlases();
    makeBossTexture();
  }
}
''')
