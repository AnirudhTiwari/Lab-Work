#include<iostream.h>
#include <stdlib.h>
#include<fstream.h>
#include "/usr/local/include/igraph/igraph.h"
int main(int argc, char* argv[]) 
{
//Code for loading adj matrix from file//
FILE *fp;
fp=fopen(argv[1], "r");

//Declaring//
igraph_bool_t directed=false;
igraph_t graph; // Graph Object
igraph_t wgraph; // Reduced Graph Object 
igraph_t igraph; 
igraph_matrix_t merges;
igraph_matrix_t am;
igraph_matrix_t rm;
igraph_matrix_t sm;
igraph_vector_t membership; // Which Node Belongs to which Cluster
igraph_real_t steps; // Number of Steps the Spliting to be done
igraph_integer_t n =0;
igraph_arpack_options_t co;
igraph_real_t modularity;
igraph_bool_t loops =true;
igraph_real_t cc; // Clustering coefficient
igraph_real_t den; // Density
igraph_integer_t dia; // Diameter
int a[16][1000];
int cl[16];
//cout<<argv[1]<<endl;
//Initialising//
igraph_vector_init(&membership,0);
igraph_matrix_init(&merges, 0,0);
igraph_matrix_init(&am,0,0);
igraph_arpack_options_init(&co);
for(int i=0;i<16;i++)
{
cl[i]=0;
}
//Loading the Graph//
igraph_read_graph_edgelist(&graph, fp, n, directed);

//Number of Edges//
igraph_real_t totedj=igraph_ecount(&graph); // Number of edges

//Getting ADJ matrix//
igraph_get_adjacency(&graph,&am,IGRAPH_GET_ADJACENCY_BOTH);

//Creating Inter Graph From AM//
igraph_adjacency(&igraph,&am,IGRAPH_ADJ_UNDIRECTED);

//Phase #1 MEJ Newman: Finding community structure using the eigenvectors of matrices//
//Divisive algorithm: each split is done by maximizing the modularity //
double max=0;
igraph_real_t mmodularity;
igraph_vector_t mmembership;
igraph_vector_init(&mmembership,0);
int maxstep;
for(int i=1;i<=1;i++)
{
	steps=i;
	igraph_community_leading_eigenvector(&graph,&merges,&membership,steps,&co); //Spliting the Graph based on the Lev vector step times
	igraph_modularity(&graph,&membership,&modularity,NULL);
	
	if(max < modularity)
	{
		max=modularity;
		maxstep=i;
		igraph_vector_update(&mmembership,&membership);
		mmodularity=modularity;
	}
}


//Extracting Clusters nodes//
	for(long int i=0;i<igraph_vector_size(&mmembership);i++)
	{
		int ti=igraph_vector_e(&mmembership,i);
		int tj=cl[ti];		
		a[ti][tj]=i;           // FINE a[][] 
		cl[ti]++;              // FINE	cl[]
	}
//Reduced Matrix//
	int cn=0; // Number of Nodes in Reduced Matrix
	for(int i=0;i<16;i++)
	{
		if(cl[i] > 0)
		cn++;                                  // FINE cn
	}
igraph_matrix_init(&rm,cn,cn);
igraph_matrix_init(&sm,cn,cn);
	float ra[cn][cn];
	for(int i=0;i<cn;i++)
	{
		for(int j=0;j<cn;j++)
		{
			int count = 0;
			if(i==j)
			{
				ra[i][j]=0;
			}
			else
			{
				for(int p=0;p<cl[i];p++)
				{
					for(int q=0;q<cl[j];q++)
					{
	
						if(igraph_matrix_e(&am,a[i][p],a[j][q])>0)
						{
							count++;
						}
					}
				}
				ra[i][j]=count;
				
			}
		}
	
	}

//Setting-Normalising-Printingnormal Reduced Matrix//
	for(int i=0;i<cn;i++)
	{
		for(int j=0;j<cn;j++)
		{
			cout<<ra[i][j]<<"\t";
			if(ra[i][j] > 0)
			{
				igraph_matrix_set(&rm,i,j,(ra[i][j]/(cl[i]+cl[j]))*100);
				igraph_matrix_set(&sm,i,j,1);
			}
		}
		cout<<endl;
	}
//Printing Normalised Reduced Matrix//
cout<<endl;
	for(int i=0;i<cn;i++)
	{
		for(int j=0;j<cn;j++)
		{
			cout<<igraph_matrix_e(&rm,i,j)<<"\t";
		}
		cout<<endl;
	}

// Clustering coefficient//
igraph_transitivity_undirected(&graph, &cc);

// Graph Density//
igraph_density(&graph, &den, loops);

// Graph Diameter//
igraph_diameter(&graph, &dia, NULL, NULL, NULL, directed, loops);

cout<<"Clustering coefficient:"<<"\t"<<cc<<endl;
cout<<"Graph Density:"<<"\t"<<den<<endl;
cout<<"Graph Diameter:"<<"\t"<<dia<<endl;

igraph_destroy(&graph);
return 0;
}

