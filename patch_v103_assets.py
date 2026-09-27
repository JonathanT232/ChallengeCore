from pathlib import Path
Path("GenerateAssets103.java").write_text(r'''import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;

public class GenerateAssets103 {
  static final Color[] COLORS={
    new Color(238,140,8), new Color(255,67,75), new Color(235,66,194), new Color(145,67,220),
    new Color(53,82,224), new Color(31,187,204), new Color(0,198,54), new Color(242,202,8)
  };

  static BufferedImage makeWheel(){
    int n=512,c=n/2,r=220;
    BufferedImage img=new BufferedImage(n,n,BufferedImage.TYPE_INT_ARGB);
    Graphics2D g=img.createGraphics();
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
    g.setStroke(new BasicStroke(12f,BasicStroke.CAP_ROUND,BasicStroke.JOIN_ROUND));
    for(int i=0;i<8;i++){
      g.setColor(COLORS[i]);
      g.fill(new Arc2D.Double(c-r,c-r,r*2,r*2,90-i*45,-45,Arc2D.PIE));
    }
    g.setColor(new Color(15,15,18));g.drawOval(c-r,c-r,r*2,r*2);
    for(int i=0;i<8;i++){
      double a=Math.toRadians(90-i*45);
      g.drawLine(c,c,(int)(c+r*Math.cos(a)),(int)(c-r*Math.sin(a)));
    }
    // glossy ring
    g.setStroke(new BasicStroke(5f));g.setColor(new Color(246,177,13));g.drawOval(c-r-5,c-r-5,r*2+10,r*2+10);
    g.setStroke(new BasicStroke(13f));g.setColor(new Color(255,255,255,70));g.drawArc(c-r+18,c-r+18,(r-18)*2,(r-18)*2,18,130);
    // sparkles
    int[][] pts={{126,150},{173,116},{378,142},{406,214},{390,350},{334,402},{166,394},{110,300},{211,78},{302,102}};
    g.setColor(new Color(255,255,255,210));
    for(int[] p:pts){g.fillOval(p[0]-5,p[1]-5,10,10);}
    // hub
    g.setColor(new Color(15,15,18));g.fillOval(c-48,c-48,96,96);
    g.setColor(new Color(249,188,7));g.fillOval(c-38,c-38,76,76);
    g.setColor(new Color(255,231,89));g.fillOval(c-24,c-24,48,48);
    g.dispose();return img;
  }

  static BufferedImage makePointer(){
    int n=180;
    BufferedImage p=new BufferedImage(n,n,BufferedImage.TYPE_INT_ARGB);
    Graphics2D g=p.createGraphics();
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
    Path2D shape=new Path2D.Double();
    shape.moveTo(18,62);shape.lineTo(98,35);shape.lineTo(151,72);shape.lineTo(139,142);shape.lineTo(34,131);shape.closePath();
    g.setColor(new Color(15,15,18));g.setStroke(new BasicStroke(11f,BasicStroke.JOIN_ROUND,BasicStroke.CAP_ROUND));g.draw(shape);
    g.setPaint(new GradientPaint(20,50,new Color(255,187,9),140,140,new Color(245,128,0)));g.fill(shape);
    g.setColor(new Color(15,15,18));g.setStroke(new BasicStroke(7f));g.draw(shape);
    // mini wheel badge
    g.setColor(new Color(15,15,18));g.fillOval(62,59,58,58);
    for(int i=0;i<6;i++){g.setColor(COLORS[i+1]);g.fill(new Arc2D.Double(69,66,44,44,90-i*60,-60,Arc2D.PIE));}
    g.setColor(new Color(255,218,26));g.fillOval(84,81,14,14);
    g.dispose();return p;
  }

  public static void main(String[] args) throws Exception {
    File gui=new File("src/main/resources/assets/challengecore/textures/gui");gui.mkdirs();
    BufferedImage src=makeWheel();
    ImageIO.write(src,"png",new File(gui,"roulette.png"));
    ImageIO.write(makePointer(),"png",new File(gui,"roulette_pointer.png"));

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
    ImageIO.write(atlas,"png",new File(gui,"roulette_atlas.png"));

    // Black/orange samurai texture with brighter gold armor accents.
    File ent=new File("src/main/resources/assets/challengecore/textures/entity");ent.mkdirs();
    BufferedImage boss=new BufferedImage(128,128,BufferedImage.TYPE_INT_ARGB);
    Graphics2D b=boss.createGraphics();
    b.setColor(new Color(10,11,13));b.fillRect(0,0,128,128);
    b.setColor(new Color(214,118,5));for(int y=0;y<128;y+=16)b.fillRect(0,y,128,4);
    b.setColor(new Color(250,178,18));for(int x=7;x<128;x+=23)b.fillRect(x,0,5,128);
    b.setColor(new Color(58,39,22));b.fillRect(0,0,32,22);b.fillRect(46,0,38,16);
    b.setColor(new Color(238,143,17));b.fillRect(4,4,23,14);b.fillRect(51,4,28,8);
    b.setColor(new Color(235,187,65));b.fillRect(42,20,30,5);b.fillRect(2,35,42,7);b.fillRect(48,35,37,7);
    b.setColor(new Color(75,76,80));b.fillRect(92,66,30,32);
    b.setColor(new Color(240,95,12));b.fillRect(2,58,34,10);b.fillRect(49,56,28,10);
    b.dispose();
    ImageIO.write(boss,"png",new File(ent,"crimson_boss.png"));
  }
}
''')
