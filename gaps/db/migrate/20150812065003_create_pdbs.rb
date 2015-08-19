class CreatePdbs < ActiveRecord::Migration
  def change
    create_table :pdbs do |t|
      t.string :name
      t.string :string
      t.string :content
      t.string :text

      t.timestamps null: false
    end
  end
end
