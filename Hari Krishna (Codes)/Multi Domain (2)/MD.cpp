#include<iostream>
#include <stdlib.h>
#include<fstream>
#include<igraph.h>
using namespace std;
int main(int argc, char* argv[]) 
{
//Code for loading adj matrix from file//
FILE *fp;
fp=fopen(argv[1], "r");
cout<<"PDB ID:"<<argv[1]<<endl;
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
int a[16][1000];
int cl[16];

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
igraph_get_adjacency(&graph,&am,IGRAPH_GET_ADJACENCY_BOTH,1);

//Creating Inter Graph From AM//
igraph_adjacency(&igraph,&am,IGRAPH_ADJ_UNDIRECTED);

//Phase #1 MEJ Newman: Finding community structure using the eigenvectors of matrices//
//Divisive algorithm: each split is done by maximizing the modularity //
double max=0;
igraph_real_t mmodularity;
igraph_vector_t mmembership;
igraph_vector_init(&mmembership,0);
int maxstep;
for(int i=1;i<=8;i++)
{
	steps=i;
	igraph_community_leading_eigenvector(&graph,0,&merges,&membership,steps,&co,0,0,0,0,0,0,0); //Spliting the Graph based on the Lev vector step times
	// igraph_community_leading_eigenvector(&graph,&merges,&membership,steps,&co); //Spliting the Graph based on the Lev vector step times
	igraph_modularity(&graph,&membership,&modularity,NULL);
	//cout<<"********************************************\n";
	//cout<<"For Split #"<<i<<" Modularity is: "<<modularity<<endl;
	//cout<<"********************************************\n";	
	//for(long int j=0;j<igraph_vector_size(&membership);j++)
	//{
		//cout<<(j+1)<<"\t"<<(VECTOR(membership)[j]+1)<<endl;
	//}
	if(max < modularity)
	{
		max=modularity;
		maxstep=i;
		igraph_vector_update(&mmembership,&membership);
		mmodularity=modularity;
	}
}

//Printing Maximum Modularity Membership vector//
cout<<"********************************************\n";
cout<<"For Split #"<<maxstep<<" Modularity is: "<<mmodularity<<endl;
cout<<"********************************************\n";
for(long int j=0;j<igraph_vector_size(&mmembership);j++)
	{
		cout<<(j+1)<<"\t"<<(VECTOR(mmembership)[j]+1)<<endl;
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

//Phase #2 Reducing the Graph ang Using Fast Greedy Algo of Newman and Moore//

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
//Creating Reduced Graph//
igraph_adjacency(&wgraph,&sm,IGRAPH_ADJ_UNDIRECTED);
cout<<"\n********************************************\n";
cout<<"Number of Nodes: "<<igraph_vcount(&wgraph)<<endl; // Number of nodes
cout<<"Number of Edges: "<<igraph_ecount(&wgraph)<<endl; // Number of edges
cout<<"********************************************\n\n";

//Fast Greedy Modularity Optimisation by Moore , Newman//

//Declaring//
igraph_matrix_t gmerges;
igraph_vector_t gmembership; // Which Node Belongs to which Cluster
igraph_vector_t gmodularity;
igraph_vector_t weights;

//Initialising//
igraph_vector_init(&gmembership,0);
igraph_matrix_init(&gmerges,0,0);
igraph_vector_init(&gmodularity,0);
igraph_vector_init(&weights,igraph_ecount(&wgraph));

//Setting Weights to the Edj's//
for(int i=0;i<igraph_ecount(&wgraph);i++)
{
	igraph_vector_set(&weights,i,1);
}
igraph_vector_t el;
igraph_vector_init(&el,0);
igraph_get_edgelist(&wgraph,&el,false);
int wc=0;
for(int i=0;i<igraph_vector_size(&el);i+=2)
{
igraph_vector_set(&weights,wc,igraph_matrix_e(&rm,igraph_vector_e(&el,i),igraph_vector_e(&el,(i+1))));
wc++;
}

igraph_community_fastgreedy(&wgraph,&weights,&gmerges,&gmodularity,0);

// igraph_community_fastgreedy(&wgraph,&weights,&gmerges,&gmodularity);
//cout<<"MODULARITY SIZE: "<<(igraph_vector_size(&gmodularity))<<endl;
//cout<<"MERGES SIZE: "<<igraph_matrix_size(&gmerges)<<endl;
//cout<<"Merges rows: "<<igraph_matrix_nrow(&gmerges)<<endl;
for(long int j=0;j<igraph_matrix_nrow(&gmerges)-1;j++)
	{
	igraph_community_to_membership(&gmerges,cn,(j+1),&gmembership,NULL);
	//cout<<"MODULARITY: "<<(VECTOR(gmodularity)[(j)])<<endl;
	//cout<<"********************************"<<endl;
	for(long int k=0;k<igraph_vector_size(&gmembership);k++)
	{
	//cout<<(k+1)<<"\t"<<(VECTOR(gmembership)[k]+1)<<endl;
	}
	}


return 0;
}

