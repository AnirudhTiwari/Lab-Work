import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Insets;
import java.util.Random;

import javax.swing.JPanel;


class plot extends JPanel {
	
	private void plot_dots(Graphics g){
		
		Graphics2D g2d = (Graphics2D) g;
		
		g2d.setColor(Color.black);
		
		Dimension size = getSize();
		
		Insets insets = getInsets();
		
		int w = size.width - insets.left - insets.right;
        int h = size.height - insets.top - insets.bottom;
        
        
        
        
       Random r = new Random();

        for (int i = 0; i < 10; i++) {

            int x = Math.abs(r.nextInt()) % w;
            int y = Math.abs(r.nextInt()) % h;
        	
             		
        		
            g2d.fillRect(x, y, 4, 4);
            
            g2d.drawLine(0, 1, 600, 0);
            
            g2d.drawLine(1, 0, 0, 600);
            
            g2d.drawLine(0, 0, 600, 600);
            
    
        }
      
       	
	}
	
	@Override
    public void paintComponent(Graphics g) {

        super.paintComponent(g);
        plot_dots(g);
    }  
	
	

}
