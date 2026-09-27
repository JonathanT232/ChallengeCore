from pathlib import Path
Path("GenerateAssets105.java").write_text(r'''import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Random;

public class GenerateAssets105 {
  static void ensure(File f){f.mkdirs();}
  static BufferedImage tex(int n, Color base, Color hi, Color lo, boolean grid){
    BufferedImage im=new BufferedImage(n,n,BufferedImage.TYPE_INT_ARGB);
    Graphics2D g=im.createGraphics();
    GradientPaint gp=new GradientPaint(0,0,hi,n,n,lo);
    g.setPaint(gp);g.fillRect(0,0,n,n);
    g.setColor(new Color(255,255,255,35));
    for(int y=2;y<n;y+=8)g.drawLine(0,y,n,y);
    if(grid){
      g.setColor(new Color(0,0,0,150));
      for(int x=4;x<n;x+=8)g.fillRect(x,0,2,n);
      for(int y=4;y<n;y+=8)g.fillRect(0,y,n,2);
    }
    g.dispose();return im;
  }
  static void write(BufferedImage im,String path)throws Exception{
    File f=new File(path);ensure(f.getParentFile());ImageIO.write(im,"png",f);
  }

  static void makeBlockTextures()throws Exception{
    String root="src/main/resources/assets/challengecore/textures/block/";
    write(tex(64,new Color(14,14,17),new Color(34,34,40),new Color(6,6,8),false),root+"slot_body.png");
    BufferedImage gold=tex(64,new Color(194,126,4),new Color(255,213,53),new Color(112,61,0),false);
    Graphics2D gg=gold.createGraphics();gg.setColor(new Color(255,242,157,120));gg.fillRect(0,4,64,4);gg.dispose();write(gold,root+"slot_gold.png");
    BufferedImage reel=tex(64,new Color(244,241,232),new Color(255,255,255),new Color(208,206,197),false);
    Graphics2D rg=reel.createGraphics();rg.setColor(new Color(22,22,25));rg.setStroke(new BasicStroke(3));rg.drawRect(1,1,62,62);rg.setColor(new Color(210,181,55));rg.drawRect(4,4,56,56);rg.dispose();write(reel,root+"slot_reel.png");
    write(tex(64,new Color(117,0,0),new Color(255,58,39),new Color(75,0,0),false),root+"slot_red.png");
    BufferedImage dark=tex(64,new Color(8,8,10),new Color(25,25,30),new Color(2,2,3),false);
    Graphics2D dg=dark.createGraphics();dg.setColor(new Color(255,190,23,80));dg.drawRect(2,2,59,59);dg.dispose();write(dark,root+"slot_dark.png");

    BufferedImage metal=tex(64,new Color(112,53,39),new Color(177,91,67),new Color(67,31,25),false);
    Graphics2D mg=metal.createGraphics();mg.setColor(new Color(223,130,89,85));for(int y=5;y<64;y+=12)mg.drawLine(0,y,64,y);mg.dispose();write(metal,root+"grill_metal.png");
    BufferedImage grate=tex(64,new Color(24,25,27),new Color(65,66,69),new Color(5,5,6),true);write(grate,root+"grill_dark.png");
    BufferedImage ember=new BufferedImage(64,64,BufferedImage.TYPE_INT_ARGB);
    Graphics2D eg=ember.createGraphics();eg.setColor(new Color(30,8,2));eg.fillRect(0,0,64,64);
    Random rr=new Random(105);
    for(int i=0;i<120;i++){
      int x=rr.nextInt(64),y=rr.nextInt(64),s=2+rr.nextInt(5);
      Color c=(i%3==0)?new Color(255,185,25):(i%3==1)?new Color(244,75,6):new Color(142,18,0);
      eg.setColor(c);eg.fillOval(x,y,s,s);
    }
    eg.dispose();write(ember,root+"grill_ember.png");
  }

  static final Color[] COLORS={
    new Color(20,207,65),new Color(255,215,31),new Color(255,150,19),new Color(255,68,74),
    new Color(255,69,193),new Color(145,72,231),new Color(56,89,233),new Color(39,196,213)
  };
  static double ease(double t){t=Math.max(0,Math.min(1,t));return 1-Math.pow(1-t,4.4);}
  static BufferedImage wheel(double angle,int outcome,double tint,double flash){
    int n=256,c=n/2,r=101;
    BufferedImage im=new BufferedImage(n,n,BufferedImage.TYPE_INT_ARGB);
    Graphics2D g=im.createGraphics();g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
    g.translate(c,c);g.rotate(Math.toRadians(angle));g.translate(-c,-c);
    for(int i=0;i<8;i++){
      Color a=COLORS[i],b=COLORS[outcome];
      int R=(int)(a.getRed()*(1-tint)+b.getRed()*tint),G=(int)(a.getGreen()*(1-tint)+b.getGreen()*tint),B=(int)(a.getBlue()*(1-tint)+b.getBlue()*tint);
      g.setColor(new Color(R,G,B));g.fill(new Arc2D.Double(c-r,c-r,r*2,r*2,90-i*45,-45,Arc2D.PIE));
    }
    g.setStroke(new BasicStroke(7f));g.setColor(new Color(14,14,16));g.drawOval(c-r,c-r,r*2,r*2);
    for(int i=0;i<8;i++){double a=Math.toRadians(90-i*45);g.drawLine(c,c,(int)(c+r*Math.cos(a)),(int)(c-r*Math.sin(a)));}
    g.setColor(new Color(246,172,9));g.setStroke(new BasicStroke(3f));g.drawOval(c-r-3,c-r-3,r*2+6,r*2+6);
    g.setColor(new Color(255,255,255,70));g.setStroke(new BasicStroke(7f));g.drawArc(c-r+9,c-r+9,(r-9)*2,(r-9)*2,20,125);
    int[][] pts={{63,73},{84,56},{190,73},{205,112},{194,174},{166,202},{84,197},{55,151}};
    g.setColor(new Color(255,255,255,220));for(int[] p:pts)g.fillOval(p[0]-3,p[1]-3,6,6);
    g.setColor(new Color(12,12,14));g.fillOval(c-24,c-24,48,48);g.setColor(new Color(246,181,9));g.fillOval(c-18,c-18,36,36);g.setColor(new Color(255,231,91));g.fillOval(c-10,c-10,20,20);
    g.translate(c,c);g.rotate(Math.toRadians(-angle));g.translate(-c,-c);

    // Fixed selector: compact yellow pointer on the upper-left rim, tip points exactly at wheel center/rim.
    Path2D tab=new Path2D.Double();
    tab.moveTo(20,58);tab.lineTo(55,45);tab.lineTo(79,57);tab.lineTo(70,82);tab.lineTo(45,88);tab.lineTo(20,77);tab.closePath();
    g.setStroke(new BasicStroke(5f,BasicStroke.JOIN_ROUND,BasicStroke.CAP_ROUND));g.setColor(new Color(15,15,18));g.draw(tab);
    g.setPaint(new GradientPaint(20,48,new Color(255,209,40),74,86,new Color(241,132,0)));g.fill(tab);g.setColor(new Color(15,15,18));g.draw(tab);
    // actual selecting tip
    Path2D tip=new Path2D.Double();tip.moveTo(69,66);tip.lineTo(84,72);tip.lineTo(71,80);tip.closePath();
    g.setColor(new Color(255,200,25));g.fill(tip);g.setColor(new Color(15,15,18));g.draw(tip);
    // mini rainbow badge
    g.setColor(new Color(15,15,18));g.fillOval(31,57,31,31);
    for(int i=0;i<6;i++){g.setColor(COLORS[(i+1)%8]);g.fill(new Arc2D.Double(35,61,23,23,90-i*60,-60,Arc2D.PIE));}
    g.setColor(new Color(255,225,50));g.fillOval(43,69,7,7);

    if(flash>0){g.setColor(new Color(255,255,255,(int)(Math.min(1,flash)*220)));g.fillOval(c-r-5,c-r-5,r*2+10,r*2+10);}
    g.dispose();return im;
  }
  static void makeRoulette()throws Exception{
    File gui=new File("src/main/resources/assets/challengecore/textures/gui");ensure(gui);
    for(int outcome=0;outcome<8;outcome++){
      BufferedImage atlas=new BufferedImage(2048,4608,BufferedImage.TYPE_INT_ARGB);Graphics2D ag=atlas.createGraphics();
      for(int f=0;f<142;f++){
        double angle,tint=0,flash=0;
        if(f<=112){double t=f/112.0;double target=360*7+outcome*45.0;angle=target*ease(t);}
        else{angle=360*7+outcome*45.0;if(f<=133)tint=(f-112)/21.0;else tint=1;if(f>=138)flash=(f-137)/4.0;}
        BufferedImage fr=wheel(angle,outcome,tint,flash);ag.drawImage(fr,(f%8)*256,(f/8)*256,null);
      }
      ag.dispose();ImageIO.write(atlas,"png",new File(gui,"roulette_"+outcome+".png"));
    }
  }

  static void makeBoss()throws Exception{
    File ent=new File("src/main/resources/assets/challengecore/textures/entity");ensure(ent);
    BufferedImage im=new BufferedImage(128,128,BufferedImage.TYPE_INT_ARGB);Graphics2D g=im.createGraphics();
    Random r=new Random(50105);
    // textured lacquered iron base
    for(int y=0;y<128;y+=2)for(int x=0;x<128;x+=2){
      int v=10+r.nextInt(24);int warm=r.nextInt(8);
      g.setColor(new Color(v+warm/2,v,v));g.fillRect(x,y,2,2);
    }
    // orange armor bands
    g.setColor(new Color(101,50,7));for(int y=0;y<128;y+=16)g.fillRect(0,y,128,4);
    g.setColor(new Color(204,108,5));for(int y=4;y<128;y+=16)g.fillRect(0,y,128,4);
    g.setColor(new Color(247,165,19));for(int x=5;x<128;x+=22)g.fillRect(x,0,4,128);
    // gold bevels
    g.setColor(new Color(255,207,67));for(int y=7;y<128;y+=18)g.fillRect(0,y,128,2);
    g.setColor(new Color(255,231,121));for(int x=8;x<126;x+=28){g.fillRect(x,4,11,2);g.fillRect(x,35,13,2);g.fillRect(x,66,9,2);}
    // gunmetal plates
    g.setColor(new Color(49,53,59));g.fillRect(0,32,46,20);g.fillRect(0,92,22,26);g.fillRect(24,92,35,26);g.fillRect(92,66,31,33);
    g.setColor(new Color(92,98,106));g.fillRect(2,34,42,3);g.fillRect(2,94,18,3);g.fillRect(27,94,29,3);
    // helmet/face/mask
    g.setColor(new Color(58,36,21));g.fillRect(0,0,32,22);g.setColor(new Color(198,122,44));g.fillRect(5,5,22,13);
    g.setColor(new Color(238,188,106));g.fillRect(8,7,16,9);
    g.setColor(new Color(8,9,10));g.fillRect(10,10,5,3);g.fillRect(19,10,5,3);
    g.setColor(new Color(210,116,8));g.fillRect(40,0,40,18);g.setColor(new Color(255,194,35));g.fillRect(42,2,36,4);
    // chest / sash / red cloth accents
    g.setColor(new Color(130,42,18));g.fillRect(49,39,33,7);g.fillRect(2,58,34,10);g.fillRect(49,56,28,10);
    g.setColor(new Color(238,142,16));g.fillRect(3,35,40,5);g.fillRect(51,34,31,4);
    g.setColor(new Color(248,195,49));g.fillRect(5,43,36,3);g.fillRect(52,46,30,3);
    // skirt plates
    g.setColor(new Color(14,15,18));g.fillRect(0,112,90,16);g.setColor(new Color(186,87,3));g.fillRect(0,114,90,5);g.setColor(new Color(244,162,21));g.fillRect(4,121,82,3);
    // steel sword area
    g.setColor(new Color(112,118,127));g.fillRect(76,52,10,38);g.setColor(new Color(225,229,235));g.fillRect(78,54,4,34);
    g.setColor(new Color(222,139,19));g.fillRect(88,52,18,22);g.setColor(new Color(87,42,7));g.fillRect(92,54,4,20);
    // rivets/studs
    g.setColor(new Color(255,226,103));for(int y=6;y<124;y+=17)for(int x=5;x<126;x+=27)g.fillRect(x,y,2,2);
    g.dispose();ImageIO.write(im,"png",new File(ent,"crimson_boss.png"));
  }

  public static void main(String[] args)throws Exception{makeBlockTextures();makeRoulette();makeBoss();}
}
''')
