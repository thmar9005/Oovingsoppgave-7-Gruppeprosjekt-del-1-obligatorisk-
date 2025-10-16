# Skriver dette bare fordi jeg vet ikke om at han siste som er igjen har gjort oppgaven eller ikke.
# Bla litt nedover for å finne opg 7 og 8. 

# Oppgave 1: 
emnekoder = []
semester = []
studiepoeng = []

def lag_nytt_emne(kode, sem, sp):
    emnekoder.append(kode)
    semester.append(sem)
    studiepoeng.append(sp)
    print(f"Emnet '{kode}' er lagt til for '{sem}' med {sp} studiepoeng.")

# Oppgave 2: 
studieplan = [[],[],[],[],[],[]]

def legg_til_emne_i_studieplan(emne_index, semester_nummer):
    if semester_nummer < 1 or semester_nummer > 6:
        print("Ugyldig nummer. Velg mellom 1-6")
        return 
    for sem in studieplan:
        if emne_index in sem:
            print("Dette emnet finnes allerede i studieplanen.")
            return
    
    emne_semester = semester[emne_index]
    if emne_semester == "høst" and semester_nummer % 2 == 0:
        print("Dette er et høstemne og kan ikke legges til i et vårsemester.")
        return
    if emne_semester == "vår" and semester_nummer % 2 == 1:
        print("Dette er et våremne og kan ikke legges til i et høstsemester.")
        return

    naavaerende_sp = sum([studiepoeng[i] for i in studieplan[semester_nummer - 1]])
    if naavaerende_sp + studiepoeng[emne_index] > 30:
        print("Ikke plass til dette emnet i semesteret, maks 30 studiepoeng")
        return
    
    studieplan[semester_nummer-1].append(emne_index)
    print(f"Emne {emnekoder[emne_index]} lagt till i semester {semester_nummer}")

# Oppgave 3:
def skriv_ut_alle_emner():
    if not emnekoder:
        print("Ingen emner er registrert ennå.")
        return
    
    print("\n--- Alle registrerte emner ---")
    for i in range(len(emnekoder)):
        print(f"{emnekoder[i]} ({semester[i]}), {studiepoeng[i]} studiepoeng")

# Oppgave 4: 
def skriv_ut_studieplan():
    print("\n--- Studieplan ---")
    for semester_nummer, emner_i_semester in enumerate(studieplan, start=1):
        if not emner_i_semester:
            print(f"Semester {semester_nummer}: (ingen emner)")
        else:
            total_poeng = sum(studiepoeng[i] for i in emner_i_semester)
            print(f"Semester {semester_nummer}:")
            for i in emner_i_semester:
                print(f"  {emnekoder[i]} ({semester[i]}), {studiepoeng[i]} studiepoeng")
            print(f"  Totalt: {total_poeng} studiepoeng\n")


# Oppgave 5:
def sjekk_gyldighet():
    gyldig = True
    for i, sem in enumerate(studieplan, start=1):
        total_sp = sum(studiepoeng[j] for j in sem)
        if total_sp == 0:
            print(f"Semester {i}: (ingen emner) → ikke gyldig (må være 30 sp)")
            gyldig = False
        elif total_sp == 30:
            print(f"Semester {i}: 30 sp ✔")
        else:
            print(f"Semester {i}: {total_sp} sp → ikke gyldig (må være 30 sp)")
            gyldig = False
    if gyldig:
        print("Hele studieplanen er gyldig.")
    else:
        print("Studieplanen er ikke gyldig (se detaljer over).")

# Oppgave 6:
import csv

def lagre_studieplan_csv(path="studieplan.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Semester", "Emnekode", "Type", "Studiepoeng"])
        for sem_nr, sem in enumerate(studieplan, start=1):
            for i in sem:
                w.writerow([sem_nr, emnekoder[i], semester[i], studiepoeng[i]])
lagre_studieplan_csv()          # lager "studieplan.csv" i prosjektmappa
# lagre_studieplan_csv("data/studieplan.csv")  # om du vil styre mappa



# oppgave 7:
def les_studieplan_csv(path="studieplan.csv"):
    emnekoder.clear()
    semester.clear()
    studiepoeng.clear()
    for sem in studieplan:
        sem.clear()

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for rad in reader:
                kode = rad["Emnekode"]
                sem_type = rad["Type"]
                sp = int(rad["Studiepoeng"])
                sem_nr = int(rad["Semester"])

                # Sjekk om emnet allerede finnes
                if kode not in emnekoder:
                    emnekoder.append(kode)
                    semester.append(sem_type)
                    studiepoeng.append(sp)
                
                # Legg til riktig indeks i studieplanen
                emne_index = emnekoder.index(kode)
                studieplan[sem_nr - 1].append(emne_index)

        print(f"Studieplan lastet inn fra '{path}' ✅")

    except FileNotFoundError:
        print(f"Fant ikke filen '{path}'. Sørg for at den er lagret først.")
    except Exception as e:
        print(f"En feil oppstod under lesing: {e}")

# Oppgave 8
def hovedmeny():
    while True:
        print("\n--- STUDIEPLAN MENY ---")
        print("1. Legg til nytt emne")
        print("2. Legg til emne i studieplan")
        print("5. Sjekk gyldighet")
        print("6. Lagre studieplan til fil")
        print("7. Les studieplan fra fil")
        print("8. Avslutt")

        valg = input("Velg et tall: ")

        if valg == "1":
            kode = input("Emnekode: ")
            sem = input("Semester (høst/vår): ")
            sp = int(input("Studiepoeng: "))
            lag_nytt_emne(kode, sem, sp)

        elif valg == "2":
            emne_index = int(input("Emneindeks (starter på 0): "))
            semester_nummer = int(input("Semester (1-6): "))
            legg_til_emne_i_studieplan(emne_index, semester_nummer)

        elif valg == "5":
            sjekk_gyldighet()

        elif valg == "6":
            lagre_studieplan_csv()

        elif valg == "7":
            les_studieplan_csv()

        elif valg == "8":
            print("Avslutter programmet. Ha en fin dag! 👋")
            break

        else:
            print("Ugyldig valg, prøv igjen.")

# TESTING:

