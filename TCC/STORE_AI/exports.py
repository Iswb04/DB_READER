def salvar_csv(df, nome="dados.csv"):
    df.to_csv(nome, index=False)
    print(f"Arquivo salvo como {nome}")