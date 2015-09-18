import java.awt.AWTException;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.GraphicsConfiguration;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.text.DecimalFormat;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.media.j3d.AmbientLight;
import javax.media.j3d.Appearance;
import javax.media.j3d.Background;
import javax.media.j3d.BoundingSphere;
import javax.media.j3d.BranchGroup;
import javax.media.j3d.Canvas3D;
import javax.media.j3d.ColoringAttributes;
import javax.media.j3d.GraphicsContext3D;
import javax.media.j3d.Group;
import javax.media.j3d.ImageComponent;
import javax.media.j3d.ImageComponent2D;
import javax.media.j3d.LineArray;
import javax.media.j3d.LineAttributes;
import javax.media.j3d.Material;
import javax.media.j3d.Raster;
import javax.media.j3d.Screen3D;
import javax.media.j3d.Shape3D;
import javax.media.j3d.Transform3D;
import javax.media.j3d.TransformGroup;
import javax.swing.JApplet;
import javax.swing.JCheckBox;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import javax.vecmath.Color3f;
import javax.vecmath.Point3d;
import javax.vecmath.Point3f;
import javax.vecmath.Vector3f;

import com.sun.j3d.utils.applet.MainFrame;
import com.sun.j3d.utils.behaviors.vp.OrbitBehavior;
import com.sun.j3d.utils.geometry.Sphere;
import com.sun.j3d.utils.geometry.Text2D;
import com.sun.j3d.utils.picking.PickCanvas;
import com.sun.j3d.utils.picking.PickResult;
import com.sun.j3d.utils.universe.PlatformGeometry;
import com.sun.j3d.utils.universe.SimpleUniverse;

class Global {

	public static String[] args;
	public static float x_center;
	public static float y_center;
	public static float z_center;

}

class molecule{

	private int unique_id;
	private int degree;
	private float x_coordinate;
	private float y_coordinate;
	private float z_coordinate;
	private int selected;
	private boolean hydrophobic;
	JCheckBox b;

	public void setx_coordinate(float x){
		x_coordinate = x;
	}

	public void sety_coordinate(float y){
		y_coordinate = y;
	}

	public void setz_coordinate(float z){
		z_coordinate=z;
	}

	public void setunique_id(int id){
		unique_id = id;
	}

	public void setselected(int num){
		selected = num;
	}

	public void set_degree(int deg){
		degree = deg;

	}

	public void set_hydrophobic(boolean hydro){
		hydrophobic = hydro;
	}


	float getx(){
		return x_coordinate;
	}

	float gety(){
		return y_coordinate;
	}

	float getz(){
		return z_coordinate;
	}


	int getid(){
		return unique_id;
	}


	int getselected(){
		return selected;
	}

	JCheckBox getbox(){
		return b;
	}

	int getdegree(){
		return degree;
	}

	public void addcheck(){
		b = new JCheckBox("ResId" + Integer.toString(getid()));
	}
}


public class tool_applet extends JApplet implements MouseListener, ItemListener,KeyListener{
	private float radius = 0.007f;
	private PickCanvas pickCanvas;
	private SimpleUniverse universe;
	private BranchGroup group = new BranchGroup();
	private	JScrollPane scrollPane;
	private	ArrayList<molecule> data = new ArrayList<molecule>();
	private GraphicsConfiguration config =SimpleUniverse.getPreferredConfiguration();
	private Canvas3D canvas = new Canvas3D(config);
	
	//	private String[] args = {"anirudh","tiwari"};
	//System.out.println(args[0]);
	//System.out.println(args[0]);

	//	args[0] = "anirudh";
	DecimalFormat myFormatter = new DecimalFormat("#.######");

	public void init(){

		//							System.out.println(args[0]);
		canvas.setSize(600,600);
		Object[][] data1;
		Container content = getContentPane();
		
		DotPlot plot = new DotPlot();
		plot.setVisible(true);

		/*	Global.args[0] = getParameter("coordinates");
			Global.args[1] = getParameter("edgelist");
			Global.args[2] = getParameter("centrality");*/
		int count = 0;
		float sum_x = 0;
		float sum_y = 0;
		float sum_z = 0;
		
		
	
	
		
	//	Canvas3D off_canvas = new Canvas3D(config, true);
	//	off_canvas.setSize(600, 600);
		

		group.setCapability(BranchGroup.ALLOW_CHILDREN_READ);
		group.setCapability(BranchGroup.ALLOW_CHILDREN_WRITE);

		group.setCapability(BranchGroup.ALLOW_CHILDREN_EXTEND);
		group.setCapability(BranchGroup.ALLOW_DETACH);
		group.setCapability(BranchGroup.ALLOW_BOUNDS_READ);
		group.setCapability(BranchGroup.ALLOW_BOUNDS_WRITE);

		universe = new SimpleUniverse(canvas);
	//	off_canvas = canvas; 
		Background background = new Background(new Color3f(1f,1f,1f));
		BoundingSphere sphere3 = new BoundingSphere(new Point3d(0,0,0), 100000);
		background.setApplicationBounds(sphere3);
		group.addChild(background);

		OrbitBehavior orbit = new OrbitBehavior(canvas,16|32);
		orbit.setSchedulingBounds(new BoundingSphere(new Point3d(200.0f,200.0f,200.0f), Double.MAX_VALUE));
		orbit.setRotFactors(0.3f,0.3f);
		orbit.setZoomFactor(0.1f);
		
		orbit.setTransXFactor(0.1f);
		orbit.setTransYFactor(0.1f);
		universe.getViewingPlatform().setViewPlatformBehavior(orbit);

		JPanel sidePanel = new JPanel();

		final Class[] classes = new Class[]{Integer.class, Integer.class,double.class,double.class,double.class};
		DefaultTableModel model = new DefaultTableModel(){

			@Override
				public Class<?> getColumnClass(int columnIndex) {
					if (columnIndex < classes.length) 
						return classes[columnIndex];
					return super.getColumnClass(columnIndex);
				}

			public boolean isCellEditable(int row, int col){ 
				return false;
			}
		}; 

		JTable table = new JTable(model); 
		model.addColumn("Resid");
		model.addColumn("Degree");
		model.addColumn("Cluster coefficient");
		model.addColumn("Closeness");
		model.addColumn("Betweenness");
		table.setAutoCreateRowSorter(true);

		scrollPane = new JScrollPane(table);
		table.setFillsViewportHeight(true);


		try{
	//	URL coord = new URL(getParameter("coordinates"));
		//	URL coord = new URL("http://10.4.3.124/GAPS/files_generated/xyz/9493_xyz.txt");
			URL coord = new URL("file:///home/tiwari/Tool_input/1BUU.pdb_xyz.txt");
			URLConnection yc = coord.openConnection();
			BufferedReader reader = new BufferedReader(new InputStreamReader(yc.getInputStream()));

	//		BufferedReader reader = new BufferedReader( new FileReader(coord));
			String line = null;
		

			while((line=reader.readLine()) != null) {


				String[] coordinates = line.split("\\s");
				int id = Integer.parseInt(coordinates[0]);
				Float x = Float.valueOf(coordinates[1]);
				Float y = Float.valueOf(coordinates[2]);
				Float z = Float.valueOf(coordinates[3]);
				Boolean hydrophobic = Boolean.valueOf(coordinates[4]);
				

				molecule a = new molecule();
				a.setunique_id(id);
				a.setx_coordinate(x/100-0.2f);
				a.sety_coordinate(y/100-0.4f);
				a.setz_coordinate(z/100+1.2f);
				a.setselected(0);
				a.set_hydrophobic(hydrophobic);

				//a.addcheck();


				data.add(a);

				Color3f black = new Color3f(0.0f, 0.0f, 0.0f);
				Color3f red = new Color3f(0.8f, 0.1f, 0.1f);
				Color3f col = new Color3f(0.0f, 0.0f, 1.0f);

				Appearance ap = new Appearance();
				ap.setCapability(Appearance.ALLOW_COLORING_ATTRIBUTES_READ);
				ap.setCapability(Appearance.ALLOW_COLORING_ATTRIBUTES_WRITE);
				ap.setCapability(Appearance.ALLOW_MATERIAL_READ);
				ap.setCapability(Appearance.ALLOW_MATERIAL_WRITE);

				ColoringAttributes ca = new ColoringAttributes(col, ColoringAttributes.NICEST); 
				ca.setCapability(ColoringAttributes.ALLOW_COLOR_WRITE);
				ca.setCapability(ColoringAttributes.ALLOW_COLOR_READ);
				ap.setColoringAttributes(ca);
				
				Material ma = new Material(black,red,black,red,1.0f);
				
				if(hydrophobic==false)
					ma = new Material(black,col,black,col,1.0f);
				
				ma.setCapability(Material.ALLOW_COMPONENT_READ);
				ma.setCapability(Material.ALLOW_COMPONENT_WRITE);
				ap.setMaterial(ma);

				Sphere sphere = new Sphere(0.007f);
				sphere.setCapability(Sphere.ENABLE_APPEARANCE_MODIFY);
				sphere.setAppearance(ap);

				Vector3f vector = new Vector3f(x/100-0.2f,y/100-0.4f,z/100+1.2f);
				TransformGroup tg = new TransformGroup();
				Transform3D transform = new Transform3D();	
				transform.setTranslation(vector);
				tg.setTransform(transform);
				tg.addChild(sphere);

				sphere.setUserData(a);
				group.addChild(tg);
				
				sum_x = sum_x + x/100-0.2f;
				sum_y = sum_y + y/100-0.4f;
				sum_z = sum_z + z/100+1.2f;

				count++;
			}
		}

		catch(IllegalArgumentException ex0 ){
			//	System.out.println("bugger!");
		}

		catch(IOException ex2){
				System.out.println("i/o exception1!!");
		}

		double[] p = {sum_x/count,sum_y/count,sum_z/count};
		Point3d center = new Point3d(p);
		orbit.setRotationCenter(center);
		

		try{
			//		System.out.println("Reading file2");
		//	URL coord = new URL(getParameter("edgelist"));
		//	URL coord = new URL("http://10.4.3.124/GAPS/files_generated/edgelist/9493_edgelist.txt");
			URL coord = new URL("file:///home/tiwari/Tool_input/1BUU_edgelist.txt");
			URLConnection yc = coord.openConnection();
			BufferedReader reader = new BufferedReader(new InputStreamReader(yc.getInputStream()));

			//			File edgelist = new File(getParameter("edgelist"));
			//			BufferedReader reader = new BufferedReader( new FileReader(edgelist));

			//			BufferedReader reader = new BufferedReader( new FileReader(edgelist));
			
			
			String line = null;
			
			ArrayList<Double> weights = new ArrayList<Double>();
			
			weights = normalize_weights(weights);
			
			int counter = 0;
	//		URL coord_copy = new URL("file:///home/tiwari/Tool_input/1N0R.pdb_edgelist.txt");
//			URLConnection yc_copy = coord_copy.openConnection();
//			BufferedReader reader_copy = new BufferedReader(new InputStreamReader(yc_copy.getInputStream()));
	//		System.out.println("check");
		//	BufferedReader reader1 = new BufferedReader(new InputStreamReader(yc.getInputStream()));
			

			while((line=reader.readLine()) != null) {

			//	System.out.println("lund");
				String[] nodes = line.split("\\s");
				int a = Integer.parseInt(nodes[0]);
				int b = Integer.parseInt(nodes[1]);
				for(int i=0;i<data.size();i++){

					if(a==i){


						for(int j=0;j<data.size();j++){
							if(b==j){
						//		System.out.println("weights "  + weights.get(counter));

								Group lineGroup = new Group();
								LineAttributes myLA = new LineAttributes( );
								LineAttributes myLA1 = new LineAttributes( );
								
								myLA.setLineWidth(2.0f);
								myLA1.setLineWidth(2.5f);
								
								Appearance app = new Appearance();
								app.setLineAttributes(myLA);
								
								Appearance back = new Appearance();
								back.setLineAttributes(myLA1);
								
								Color3f line_colour = new Color3f(0.0f,1.0f,0.0f);
								Color3f backbone_colour = new Color3f(0.0f,0.0f,1.0f);
								
								
								int option = 0;
			//Un-comment the below commented code snippet for changing the weights based on the edge's width.					
				
							if(option==1){
				
								if(weights.get(counter) <= 0.20){
										myLA.setLineWidth(2.0f);
									    myLA1.setLineWidth(2.0f);
	
									}
									
									if(weights.get(counter) > 0.20 && weights.get(counter) <= 0.40){
										myLA.setLineWidth(3.0f);
										myLA1.setLineWidth(3.0f);
	
									}
									
									if(weights.get(counter) > 0.40 && weights.get(counter) <= 0.60 ){
										myLA.setLineWidth(4.0f);
										myLA1.setLineWidth(4.0f);
									}
									
									if(weights.get(counter) > 0.60 && weights.get(counter) <= 0.80 ){
										myLA.setLineWidth(5.0f);
										myLA1.setLineWidth(5.0f);
									}
									
									if(weights.get(counter) > 0.80 && weights.get(counter) <= 1.00 ){
										myLA.setLineWidth(6.0f);
										myLA1.setLineWidth(6.0f);
									}
									
						
							}
				//End of width based weights code snippet.	
								
								
								
								
				//Start of colour based weights code snippet.	
								

									
								
								if(option==2){

										if(weights.get(counter) <= 0.20){
										
											 line_colour = new Color3f(0.0f,1.0f,0.0f);
											 backbone_colour = new Color3f(0.0f,1.0f,0.0f);

										}
										
										if(weights.get(counter) > 0.20 && weights.get(counter) <= 0.40){
										
											 line_colour = new Color3f(0.0f,0.0f,1.0f);
											 backbone_colour = new Color3f(0.0f,0.0f,1.0f);
											
										}
										
										if(weights.get(counter) > 0.40 && weights.get(counter) <= 0.60 ){
											 line_colour = new Color3f(1.0f,1.0f,0.0f);
											 backbone_colour = new Color3f(1.0f,1.0f,0.0f);
										}
										
										if(weights.get(counter) > 0.60 && weights.get(counter) <= 0.80 ){
											
											 line_colour = new Color3f(0.0f,1.0f,1.0f);
											 backbone_colour = new Color3f(0.0f,1.0f,1.0f);
										}
										
										if(weights.get(counter) > 0.80 && weights.get(counter) <= 1.00 ){
											 line_colour = new Color3f(1.0f,0.0f,1.0f);
											 backbone_colour = new Color3f(1.0f,0.0f,1.0f);
										}
									
								}
						//End of colour based weights code snippet. 
								if(option==3){
									
						
						//			System.out.println("lo bhai blue " + Maxblue);
									
								
									if(weights.get(counter) <= 0.10){
										
										
										 line_colour = new Color3f(0.0f,0.0f,0.1f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.1f);

									}
									
									if(weights.get(counter) > 0.10 && weights.get(counter) <= 0.20){
									
										 line_colour = new Color3f(0.0f,0.0f,0.2f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.2f);
										
									}
									
									if(weights.get(counter) > 0.20 && weights.get(counter) <= 0.30 ){
										 line_colour = new Color3f(0.0f,0.0f,0.3f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.3f);
									}
									
									if(weights.get(counter) > 0.30 && weights.get(counter) <= 0.40 ){
										
										 line_colour = new Color3f(0.0f,0.0f,0.4f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.4f);
									}
									
									if(weights.get(counter) > 0.40 && weights.get(counter) <= 0.50 ){
										 line_colour = new Color3f(0.0f,0.0f,0.5f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.5f);
									}					
									
									if(weights.get(counter) > 0.50 && weights.get(counter) <= 0.60 ){
										 line_colour = new Color3f(0.0f,0.0f,0.6f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.6f);
									}					
									
									if(weights.get(counter) > 0.60 && weights.get(counter) <= 0.70 ){
										 line_colour = new Color3f(0.0f,0.0f,0.7f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.7f);
									}					
									
									if(weights.get(counter) > 0.70 && weights.get(counter) <= 0.80 ){
										 line_colour = new Color3f(0.0f,0.0f,0.8f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.8f);
									}					
									
									if(weights.get(counter) > 0.80 && weights.get(counter) <= 0.90 ){
										 line_colour = new Color3f(0.0f,0.0f,0.9f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.9f);
									}					
									
									if(weights.get(counter) > 0.90 && weights.get(counter) <= 1.0 ){
										 line_colour = new Color3f(0.0f,0.0f,1.0f);
										 backbone_colour = new Color3f(0.0f,0.0f,1.0f);
									}					
									
									
								}
									
								if(option==4){
									if(weights.get(counter) <= 0.20){
										
										 line_colour = new Color3f(0.0f,0.0f,0.1f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.1f);

									}
									
									if(weights.get(counter) > 0.20 && weights.get(counter) <= 0.40){
									
										 line_colour = new Color3f(0.0f,0.0f,0.3f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.3f);
										
									}
									
									if(weights.get(counter) > 0.40 && weights.get(counter) <= 0.60 ){
										 line_colour = new Color3f(0.0f,0.0f,0.5f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.5f);
									}
									
									if(weights.get(counter) > 0.60 && weights.get(counter) <= 0.80 ){
										
										 line_colour = new Color3f(0.0f,0.0f,0.7f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.7f);
									}
									
									if(weights.get(counter) > 0.80 && weights.get(counter) <= 1.00 ){
										 line_colour = new Color3f(0.0f,0.0f,0.9f);
										 backbone_colour = new Color3f(0.0f,0.0f,0.9f);
									}
								
									
									
									
								}
								
								
								ColoringAttributes ca = new ColoringAttributes();
								ColoringAttributes cb = new ColoringAttributes();
								
								cb.setColor(backbone_colour);
								ca.setColor(line_colour);
								
								app.setColoringAttributes(ca);
								back.setColoringAttributes(cb);
								
								Point3f[] plaPts = new Point3f[2];
								plaPts[0] = new Point3f(data.get(i).getx(), data.get(i).gety(),data.get(i).getz());
								plaPts[1] = new Point3f(data.get(j).getx(), data.get(j).gety(),data.get(j).getz());
								LineArray pla = new LineArray(2, LineArray.COORDINATES);
								
								pla.setCoordinates(0, plaPts);
								if(b-a==1){							
									Shape3D plShape = new Shape3D(pla, back); 
									group.addChild(plShape);
								}
								else
								{
									Shape3D line_connect = new Shape3D(pla, app);
									group.addChild(line_connect);
								}
							}
						}
					}
				}
				counter++;
			}
		}

		catch(IllegalArgumentException ex0 ){
			//			System.out.println("bugger!");
		}

		catch(IOException ex2){
						System.out.println(ex2);
		}

		try{
			//			System.out.println(Global.args[1]);
		//	URL coord = new URL(getParameter("centrality"));
		//	URL coord = new URL("http://10.4.3.124/GAPS/files_generated/centrality/9493_centrality.txt");
			 URL coord = new URL("file:///home/tiwari/Tool_input/1N0R_centrality.txt");
			URLConnection yc = coord.openConnection();
			BufferedReader reader = new BufferedReader(new InputStreamReader(yc.getInputStream()));

			//			File centrality = new File(getParameter("centrality"));
			//			BufferedReader reader = new BufferedReader( new FileReader(centrality));
			String line = null;
			int i;

			for(i=-1;i<data.size();i++) {

				if((line=reader.readLine()) == null){
					
					break;
				}

				else if(i>=0){
					String[] coordinates = line.split("\\s");
					int residue = data.get(i).getid();
					int degree = Integer.parseInt(coordinates[2]);
					double cluster_coefficient = Double.parseDouble(coordinates[4]);
					double closeness = Double.parseDouble(coordinates[5]);
					double betweeness = Double.parseDouble(coordinates[6]); 
					String output = myFormatter.format(betweeness);
					data.get(i).set_degree(degree);
					data.get(i).addcheck();
					data.get(i).getbox().addItemListener(this);
					model.addRow(new Object[]{
							residue, degree, cluster_coefficient, closeness, output});

				}

			}
		}

		catch(IllegalArgumentException ex0 ){
			System.out.println(ex0);
		}

		catch(IOException ex2){
			System.out.println("i/o exception!!");
		}

		//		for(int i=0;i<data.size();i++){
		//			System.out.println(data.get(i).getdegree());
		//		}


		Color3f ambientColour = new Color3f(1.0f, 0.0f, 0.0f);
		//		Color3f spotColour = new Color3f(1.0f, 1.0f, 1.0f);
		BoundingSphere bounds =	new BoundingSphere(new Point3d(0.0,0.0,0.0), 100.0);
		AmbientLight ambientLight = new AmbientLight(ambientColour);
		ambientLight.setInfluencingBounds(bounds);	
		group.addChild(ambientLight);


		pickCanvas = new PickCanvas(canvas, group);
		pickCanvas.setMode(PickCanvas.GEOMETRY);
		pickCanvas.setTolerance(0.07f);
		canvas.addMouseListener(this);
		 
	    canvas.addKeyListener(this);
		content.setBackground(Color.black);
	//	off_canvas.setBackground(Color.black);
		//sidePanel.add(scrollPane, BorderLayout.EAST);



		//JPanel controlArea = new JPanel(new GridLayout(3, 1));
		/*sidePanel.add(new JButton("Button 1"));
		  sidePanel.add(new JButton("Button 2"));
		  sidePanel.add(new JButton("Button 3"));*/
		content.add(canvas,BorderLayout.NORTH);
	//	content.add(off_canvas,BorderLayout.NORTH);
		content.add(scrollPane);

		//		content.add(canvas,BorderLayout.SOUTH);
		universe.getViewingPlatform().setNominalViewingTransform();
		universe.addBranchGraph(group);

		

	
	}

	private ArrayList<Double> normalize_weights(ArrayList<Double> weights) throws IOException {
		// TODO Auto-generated method stub
		
		URL coord = new URL("file:///home/tiwari/Tool_input/1BUU_edgelist.txt");
		URLConnection yc = coord.openConnection();
		BufferedReader reader = new BufferedReader(new InputStreamReader(yc.getInputStream()));
		
		String line = null;
		Double max = 0.0;
		int i;
		
		try {
			while((line=reader.readLine()) != null) {

				String[] nodes = line.split("\\s");
				Double a = Double.parseDouble(nodes[2]);
	//			System.out.println(a);
				if(a > max){
					max = a;
				}
				weights.add(a);
				
			}
	
	//		System.out.println("This is the fucking max " + max);
			
			for(i=0;i<weights.size();i++){
				
			
				Double temp = weights.get(i);
				weights.set(i,temp/max);
				
	//			System.out.println("values rollin biatch " + weights.get(i));
				
			}
			
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return weights;
	}

	public void mouseClicked(MouseEvent e)
	{
		ItemEvent x;
		JCheckBox box;
		BranchGroup group2 = new BranchGroup();
		pickCanvas.setShapeLocation(e);
		PickResult result = pickCanvas.pickClosest();

		if (result == null) {
			//		System.out.println("Nothing picked");
		} 

		else {
			Sphere p = (Sphere)result.getNode(PickResult.PRIMITIVE);
			//			System.out.println(p.getCapability());


			if (p != null) {
				radius = radius + 0.000001f;

				molecule test = new molecule();
				test=(molecule)p.getUserData();
				//	System.out.println(test.getselected());
				if(test.getselected()==0){
					//	test.setselected(1);
					box = test.getbox();
					box.doClick();

					//			System.out.println(box.getselected());
					//			box.setselected(1);
					//			box.Checked = !box.Checked;
					//					itemStateChanged(box);
				}
				else{
					//	test.setselected(0);
					box = test.getbox();
					box.doClick();
				}

				float temp_x = test.getx();
				float temp_y = test.gety();
				float temp_z = test.getz();

				Sphere sphere1 = new Sphere(radius);
				Appearance ap1 = new Appearance();
				ap1.setCapability(Appearance.ALLOW_COLORING_ATTRIBUTES_READ);
				ap1.setCapability(Appearance.ALLOW_COLORING_ATTRIBUTES_WRITE);

				TransformGroup tg1 = new TransformGroup();
				Transform3D transform1 = new Transform3D();

				Color3f black = new Color3f(0.0f, 0.0f, 0.0f);
				Color3f red = new Color3f(0.8f, 0.1f, 0.1f);
				Color3f col = new Color3f(0.0f, 0.0f, 1.0f);

				ColoringAttributes ca1 = new ColoringAttributes(col, ColoringAttributes.NICEST); 
				ap1.setColoringAttributes(ca1);

				Material ma1 = new Material(black,black,black,black, 1.0f);
				Material ma2 = new Material(black,red,black,red,1.0f);

				/*	if(test.getselected() == 1){
					ap1.setMaterial(ma1);
					}

					else{
					ap1.setMaterial(ma2);
					}
				 */
				sphere1.setAppearance(ap1);
				Vector3f vector = new Vector3f(temp_x,temp_y,temp_z);
				TransformGroup tg = new TransformGroup();
				Transform3D transform = new Transform3D();	
				transform.setTranslation(vector);
				tg.setTransform(transform);
				tg.addChild(sphere1);

				group2.addChild(tg);
				universe.addBranchGraph(group2);

				PlatformGeometry pg = new PlatformGeometry();
				TransformGroup objScale = new TransformGroup();

				Transform3D t3d = new Transform3D();
				t3d.setTranslation(new Vector3f(+1.0f,0.45f,-3.0f));
				objScale.setTransform(t3d);

				Text2D text = new Text2D("Resid:" + test.getid(), black, "Ariel", 12, 0);

				objScale.addChild(text);
				pg.addChild(objScale);
				universe.getViewingPlatform().setPlatformGeometry(pg);
				
				


				//		System.out.println("Resid:" + test.getid());
			} 

			else{
				//			System.out.println("null");
			}
		}
	}

	public void mousePressed(MouseEvent e) {
	}

	public void mouseReleased(MouseEvent e) {
	}

	public void mouseEntered(MouseEvent e) {
	}

	public void mouseExited(MouseEvent e) {
	}

	public void itemStateChanged(ItemEvent e) {
		BranchGroup group3 = new BranchGroup();
		String[] params = e.paramString().split(",");
		String[] a = params[params.length - 2].split("");

		String no = "";

		for(int i = 11; i < a.length - 1; i++)
		{
			no = no + a[i];
		}
		//	System.out.println(no);

		int id = Integer.parseInt(no);

		for(int i=0;i<data.size();i++){

			if(data.get(i).getid()==id){
				radius = radius + 0.000001f;
				if(data.get(i).getselected() == 1){
					data.get(i).setselected(0);
				}

				else {
					data.get(i).setselected(1);
				}
				molecule test = new molecule();
				test = data.get(i);

				float temp_x = test.getx();
				float temp_y = test.gety();
				float temp_z = test.getz();

				Sphere sphere1 = new Sphere(radius);
				Appearance ap1 = new Appearance();
				ap1.setCapability(Appearance.ALLOW_COLORING_ATTRIBUTES_READ);
				ap1.setCapability(Appearance.ALLOW_COLORING_ATTRIBUTES_WRITE);

				TransformGroup tg1 = new TransformGroup();
				Transform3D transform1 = new Transform3D();

				Color3f black = new Color3f(0.0f, 0.0f, 0.0f);
				Color3f red = new Color3f(0.8f, 0.1f, 0.1f);
				Color3f col = new Color3f(0.0f, 0.0f, 1.0f);

				ColoringAttributes ca1 = new ColoringAttributes(col, ColoringAttributes.NICEST); 
				ap1.setColoringAttributes(ca1);

				Material ma1 = new Material(black,black,black,black, 1.0f);
				Material ma2 = new Material(black,red,black,red,1.0f);

				if(test.getselected() == 1){
					ap1.setMaterial(ma1);
				}

				else{
					ap1.setMaterial(ma2);
				}

				sphere1.setAppearance(ap1);
				Vector3f vector = new Vector3f(temp_x,temp_y,temp_z);
				TransformGroup tg = new TransformGroup();
				Transform3D transform = new Transform3D();	
				transform.setTranslation(vector);
				tg.setTransform(transform);
				tg.addChild(sphere1);

				PlatformGeometry pg = new PlatformGeometry();
				TransformGroup objScale = new TransformGroup();

				Transform3D t3d = new Transform3D();
				t3d.setTranslation(new Vector3f(1.0f,0.6f,-3.0f));
				objScale.setTransform(t3d);

				Text2D text = new Text2D("Resid:" + test.getid(), black, "Ariel", 12, 0);

				objScale.addChild(text);
				pg.addChild(objScale);

				group3.addChild(tg);
				universe.addBranchGraph(group3);
				universe.getViewingPlatform().setPlatformGeometry(pg);
				
				
				

				//		System.out.println("Resid:" + test.getid());
			}
		}	
	}

	public static void main(String Args[]){	
		//		for (String s: Args) {
		//            System.out.println(args[1]);
		//      }
		//  		Global.args = Args;	




		tool_applet a = new tool_applet();
		//		a.init(Args[]);
		MainFrame mf = new MainFrame(a, 600, 600);

	}

	@Override
	public void keyPressed(KeyEvent e) {
		take_screenshot(e);
		
		// TODO Auto-generated method stub
	}

	private void take_screenshot(KeyEvent p) {
		// TODO Auto-generated method stub
		
		char key = p.getKeyChar();
		
		if(key == 'P'){
			System.out.println("You took a screen shot!!");
			
			 Canvas3D off_canvas = new Canvas3D(config,true);
			 Screen3D s_on = canvas.getScreen3D();
			 Screen3D s_off = off_canvas.getScreen3D();
			 
			 Dimension dim = s_on.getSize();
	

			 s_off.setSize(dim);
			 s_off.setPhysicalScreenWidth(s_on.getPhysicalScreenWidth()
			          * 3);
			 s_off.setPhysicalScreenHeight(s_on.getPhysicalScreenHeight()
			          * 3);
			 
			 universe.getViewer().getView().addCanvas3D(off_canvas);
		      
		    BufferedImage bImage = new BufferedImage(dim.width, dim.height,
		            BufferedImage.TYPE_INT_ARGB);

		        ImageComponent2D buffer = new ImageComponent2D(
		            ImageComponent.FORMAT_RGBA, bImage);

		        off_canvas.setOffScreenBuffer(buffer);
		        off_canvas.renderOffScreenBuffer();
		        off_canvas.waitForOffScreenRendering();
		        bImage = off_canvas.getOffScreenBuffer().getImage();

		    try {
				ImageIO.write(bImage, "png", new File("/home/tiwari/Desktop/test.png"));
				
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			
			
		/*	try {
				Robot robot = new Robot();
				BufferedImage bi=robot.createScreenCapture(new Rectangle(1400,650));
			    ImageIO.write(bi, "jpg", new File("/home/tiwari/Desktop/test.jpg"));
			    
				
			} catch (AWTException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}*/
		}
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyTyped(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}


}

