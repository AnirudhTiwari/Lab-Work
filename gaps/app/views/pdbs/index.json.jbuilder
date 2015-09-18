json.array!(@pdbs) do |pdb|
  json.extract! pdb, :id, :name, :string, :content, :text
  json.url pdb_url(pdb, format: :json)
end
