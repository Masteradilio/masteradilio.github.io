from pathlib import Path


def patch(path: str, replacements: list[tuple[str, str]]) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"Updated {path}")
    else:
        print(f"No changes required for {path}")


patch(
    "assets/cv_adilio_farias_en.html",
    [
        (
            "<title>Resume - Adilio de Sousa Farias - Senior Data Scientist</title>",
            "<title>Resume - Adilio de Sousa Farias - AI Engineer & Senior Data Scientist</title>",
        ),
        (
            "SENIOR DATA SCIENTIST | MACHINE LEARNING | FRAUD | CREDIT RISK | MLOPS",
            "AI ENGINEER | SENIOR DATA SCIENTIST | MACHINE LEARNING | MLOPS | GENERATIVE AI",
        ),
        (
            "Brasília, Federal District, Brazil | Open to Hybrid & Remote",
            "Brasília, Federal District, Brazil | Open to Remote Opportunities",
        ),
        (
            "Senior Data Scientist with 15+ years of experience in the financial sector,",
            "AI Engineer and Senior Data Scientist with 15+ years of experience in the financial sector,",
        ),
        (
            "<div class=\"item-sub\">Data Scientist & Machine Learning | Brasília, Federal District, Brazil</div>",
            "<div class=\"item-sub\">AI and Machine Learning Engineer | Brasília, Federal District, Brazil</div>",
        ),
    ],
)

patch(
    "assets/cv_adilio_farias_en.txt",
    [
        (
            "Senior Data Scientist | Machine Learning | Fraud | Credit Risk | MLOps",
            "AI Engineer | Senior Data Scientist | Machine Learning | MLOps | Generative AI",
        ),
        (
            "Brasília, Federal District, Brazil | Open to Hybrid & Remote",
            "Brasília, Federal District, Brazil | Open to Remote Opportunities",
        ),
        (
            "Senior Data Scientist with 15+ years of experience in the financial sector,",
            "AI Engineer and Senior Data Scientist with 15+ years of experience in the financial sector,",
        ),
        (
            "Data Scientist & Machine Learning | Brasília, Federal District, Brazil",
            "AI and Machine Learning Engineer | Brasília, Federal District, Brazil",
        ),
    ],
)

patch(
    "assets/cv_adilio_farias_pt.html",
    [
        (
            "<title>Curriculo - Adilio de Sousa Farias - Cientista de Dados Senior</title>",
            "<title>Curriculo - Adilio de Sousa Farias - Engenheiro de IA e Cientista de Dados Senior</title>",
        ),
        (
            "CIENTISTA DE DADOS SÊNIOR | MACHINE LEARNING | FRAUDE | RISCO DE CRÉDITO | MLOPS",
            "ENGENHEIRO DE IA | CIENTISTA DE DADOS SÊNIOR | MACHINE LEARNING | MLOPS | IA GENERATIVA",
        ),
        (
            "Cientista de Dados com mais de 15 anos de experiência no setor financeiro,",
            "Engenheiro de IA e Cientista de Dados com mais de 15 anos de experiência no setor financeiro,",
        ),
        (
            "<div class=\"item-sub\">Cientista de Dados e Machine Learning | Brasília/DF</div>",
            "<div class=\"item-sub\">Engenheiro de IA e Machine Learning | Brasília/DF</div>",
        ),
    ],
)

patch(
    "assets/cv_adilio_farias_pt.txt",
    [
        (
            "Cientista de Dados Sênior | Machine Learning | Fraude | Risco de Crédito | MLOps",
            "Engenheiro de IA | Cientista de Dados Sênior | Machine Learning | MLOps | IA Generativa",
        ),
        (
            "Cientista de Dados com mais de 15 anos de experiência no setor financeiro,",
            "Engenheiro de IA e Cientista de Dados com mais de 15 anos de experiência no setor financeiro,",
        ),
        (
            "Cientista de Dados e Machine Learning | Brasília/DF",
            "Engenheiro de IA e Machine Learning | Brasília/DF",
        ),
    ],
)
