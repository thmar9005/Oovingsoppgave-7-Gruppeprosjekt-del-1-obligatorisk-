### DEL 2:

# opg a:

class Emne:
    def __init__(self, kode, navn, semester, studiepoeng, eksamensform=None, beskrivelse=None):
        self.kode = kode
        self.navn = navn
        self.semester = semester.upper() 
        self.studiepoeng = studiepoeng
        self.eksamensform = eksamensform
        self.beskrivelse = beskrivelse
        
    def __str__(self):
        if self.semester == "H":
            sem_full = "høst"
        else:
            sem_full = "vår"
        return f"{self.kode} - {self.navn} ({sem_full}), {self.studiepoeng} studiepoeng."

### DEL 1: 

# Oppgave 1: 

# emnekoder = []
# semester = []
# studiepoeng = []

emner = []
studieplan = [[],[],[],[],[],[]]

# Endring i lag_nytt_emne(); nye variabler. 
def lag_nytt_emne(kode, navn, semester, studiepoeng, eksamensform=None, beskrivelse=None):
    nytt_emne = Emne(kode, navn, semester, studiepoeng, eksamensform, beskrivelse)
    emner.append(nytt_emne)
    print(f"Emnet '{kode}' er lagt til for '{nytt_emne.semester}' med {studiepoeng} studiepoeng.")

# Oppgave 2: 

def legg_til_emne_i_studieplan(emne_index, semester_nummer):
    if semester_nummer < 1 or semester_nummer > 6:
        print("Ugyldig nummer. Velg mellom 1-6")
        return 
    
    for sem in studieplan:
        if emne_index in sem:
            print("Dette emnet finnes allerede i studieplanen.")
            return
    
    emne = emner[emne_index]

    # Høst = "H", Vår = "V"
    if emne.semester == "H" and semester_nummer % 2 == 0:
        print("Dette er et høstemne og kan ikke legges til i et vårsemester.")
        return
    if emne.semester == "V" and semester_nummer % 2 == 1:
        print("Dette er et våremne og kan ikke legges til i et høstsemester.")
        return

    naavaerende_sp = sum([emner[i].studiepoeng for i in studieplan[semester_nummer - 1]])
    if naavaerende_sp + emne.studiepoeng > 30:
        print("Ikke plass til dette emnet i semesteret, maks 30 studiepoeng")
        return
    
    studieplan[semester_nummer-1].append(emne_index)
    print(f"Emne {emne.kode} lagt til i semester {semester_nummer}")

# Oppgave 3:
def skriv_ut_alle_emner():
    if not emner:
        print("Ingen emner er registrert ennå.")
        return
    
    print("\n--- Alle registrerte emner ---")
    for i, e in enumerate(emner): # Både element og indeks går gjennom emner-listen
        print(f"[{i}] {e}")

# Oppgave 4: 
def skriv_ut_studieplan():
    print("\n--- Studieplan ---")
    for semester_nummer, emner_i_semester in enumerate(studieplan, start=1):
        if not emner_i_semester:
            print(f"Semester {semester_nummer}: (ingen emner)")
        else:
            total_poeng = sum(emner[i].studiepoeng for i in emner_i_semester)
            print(f"Semester {semester_nummer}:")
            for i in emner_i_semester:
                e = emner[i]
                if e.semester == "H":
                    sem_full = "høst"
                else:
                    sem_full = "vår"
                print(f"  {e.kode} - {e.navn} ({sem_full}), {e.studiepoeng} studiepoeng")
            print(f"  Totalt: {total_poeng} studiepoeng\n")

# Oppgave 5:
def sjekk_gyldighet():
    gyldig = True
    for i, sem in enumerate(studieplan, start=1):
        total_sp = sum(emner[j].studiepoeng for j in sem)
        if total_sp == 0:
            print(f"Semester {i}: (ingen emner) -> ikke gyldig (må være 30 sp)")
            gyldig = False
        elif total_sp == 30:
            print(f"Semester {i}: 30 sp")
        else:
            print(f"Semester {i}: {total_sp} sp -> ikke gyldig (må være 30 sp)")
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
        w.writerow(["Semester", "Emnekode", "Navn", "Type", "Studiepoeng"])
        for sem_nr, sem in enumerate(studieplan, start=1):
            for i in sem:
                e = emner[i]
                w.writerow([sem_nr, e.kode, e.navn, e.semester, e.studiepoeng])
    print(f"studieplan lagret til '{path}' ")
# lagre_studieplan_csv()          # lager "studieplan.csv" i prosjektmappa
# lagre_studieplan_csv("data/studieplan.csv")  # om du vil styre mappa



# oppgave 7:
def les_studieplan_csv(path="studieplan.csv"):
    emner.clear()
    for sem in studieplan:
        sem.clear()

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for rad in reader:
                kode = rad["Emnekode"]
                navn = rad["Navn"]
                sem_type = rad["Type"].upper()
                sp = int(rad["Studiepoeng"])
                sem_nr = int(rad["Semester"])

                # Sjekk om emnet allerede finnes
                eksisterende_index = None
                for i in range(len(emner)):
                    if emner[i].kode == kode:
                        eksisterende_index = i
                        break
                    
                if eksisterende_index is None:                    
                    e = Emne(kode, navn, sem_type, sp)
                    emner.append(e)
                    eksisterende_index = len(emner) - 1
                
                # Legg til riktig indeks i studieplanen
                studieplan[sem_nr - 1].append(eksisterende_index)

        print(f"Studieplan lastet inn fra '{path}'...")

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
        print("3. Skriv ut alle registrerte emner")
        print("4. Skriv ut studieplanen")
        print("5. Sjekk gyldighet")
        print("6. Lagre studieplan til fil")
        print("7. Les studieplan fra fil")
        print("8. Avslutt")

        valg = input("Velg et tall: ")

        if valg == "1":
            kode = input("Emnekode: ")
            navn = input("Navn: ")
            sem = input("Semester (H/V): ")
            sp = int(input("Studiepoeng: "))
            lag_nytt_emne(kode, navn, sem, sp)

        elif valg == "2":
            emne_index = int(input("Emneindeks (starter på 0): "))
            semester_nummer = int(input("Semester (1-6): "))
            legg_til_emne_i_studieplan(emne_index, semester_nummer)

        elif valg == "3":
            skriv_ut_alle_emner()

        elif valg == "4":
            skriv_ut_studieplan()

        elif valg == "5":
            sjekk_gyldighet()

        elif valg == "6":
            lagre_studieplan_csv()

        elif valg == "7":
            les_studieplan_csv()

        elif valg == "8":
            print("Avslutter programmet. Ha en fin dag!")
            break

        else:
            print("Ugyldig valg, prøv igjen.")

# TESTING:

if __name__ == "__main__":
    hovedmeny()
