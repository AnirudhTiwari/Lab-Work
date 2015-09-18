class PdbsController < ApplicationController
  before_action :set_pdb, only: [:show, :edit, :update, :destroy]

  # GET /pdbs
  # GET /pdbs.json
  def index
    @pdbs = Pdb.all
  end

  # GET /pdbs/1
  # GET /pdbs/1.json
  def show
  end

  # GET /pdbs/new
  def new
    @pdb = Pdb.new
  end

  # GET /pdbs/1/edit
  def edit
  end

  # POST /pdbs
  # POST /pdbs.json
  def create
    @pdb = Pdb.new(pdb_params)

    respond_to do |format|
      if @pdb.save
        format.html { redirect_to @pdb, notice: 'Pdb was successfully created.' }
        format.json { render :show, status: :created, location: @pdb }
      else
        format.html { render :new }
        format.json { render json: @pdb.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /pdbs/1
  # PATCH/PUT /pdbs/1.json
  def update
    respond_to do |format|
      if @pdb.update(pdb_params)
        format.html { redirect_to @pdb, notice: 'Pdb was successfully updated.' }
        format.json { render :show, status: :ok, location: @pdb }
      else
        format.html { render :edit }
        format.json { render json: @pdb.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /pdbs/1
  # DELETE /pdbs/1.json
  def destroy
    @pdb.destroy
    respond_to do |format|
      format.html { redirect_to pdbs_url, notice: 'Pdb was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_pdb
      @pdb = Pdb.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def pdb_params
      params.require(:pdb).permit(:name, :string, :content, :text)
    end
end
