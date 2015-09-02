import javax.swing.JFrame;



public class DotPlot extends JFrame{
	
	public DotPlot(){
		
		initUI();
	}
	
	public void initUI(){
		
		setTitle("DotPlot");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		add(new plot());
		
		setSize(600, 600);
		setLocationRelativeTo(null);	
		
	}
	
   /* public static void main(String[] args) {

        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {

                DotPlot ps = new DotPlot();
                ps.initUI();
                ps.setVisible(true);
            }
        });
    }*/
}
