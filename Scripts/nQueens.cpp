bool checkValid(vector< vector<int> > &board, int row, int col){
        for(int i=row;i<board.size();i++){
            if(board[row][i]==1)
                return false;
        }
        
        for(int i=col;i<board.size();i++){
            if(board[i][col]==1)
                return false;
        }
        
        int i=row, j=col;
        while(i < board.size() && j < board.size()){
            if(board[i][j]==1)
                return false;
            i++;
            j++;
        }
        
        i=row;j=col;
        while(i > -1 && j > -1){
            if(board[i][j]==1)
                return false;
            i--;
            j--;
        }
        
        i=row;j=col;
        while(i > -1 && j < board.size()){
            if(board[i][j]==1)
                return false;
            i--;
            j++;
        }
        
        i=row;j=col;
        while(i < board.size() && j > -1){
            if(board[i][j]==1)
                return false;
            i++;
            j--;
        }
        return true;
    }
    
    vector<string> convertToBoard(vector< vector<int> > &board){
        int i,j;
        
        string row;
        
        vector<string> chessBoard;
        
        for(i=0; i<board.size(); i++){
           row.clear();
           for(j=0; j<board.size(); j++){
               
               if(board[i][j]==0)
                    row = row + '.';
               else
                    row = row + 'Q';
                    
           }
           chessBoard.push_back(row);
        }
        return chessBoard;
    }
    
    void placeQueens(vector< vector<string> > &ans, vector< vector<int> > &board, int row, int q){
        
        if(q==0){
            ans.push_back(convertToBoard(board));
            return;
        }
            
        
        for(int j=0; j<board.size(); j++){
            if(checkValid(board, row, j))
                placeQueens(ans, board, row+1, q-1);
            
        }
        
        return;
            
    }
    
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<int> > board(0, vector<int> (n, 0));
        
        vector<vector<string> > ans;
        
        int queens = n;
        
        placeQueens(ans,board,0,n);
        
        return ans;
    }