# 1. 
emnekoder = []
semester = []
studiepoeng = []

def lag_nytt_emne(kode, sem, sp):
    emnekoder.append(kode)
    semester.append(sem)
    studiepoeng.append(sp)
    print(f"Emnet '{kode}' er lagt til for '{sem}' med {sp} studiepoeng.")

# 2. 
studieplan = [[],[],[],[],[],[]]

def legg_til_emne_i_studieplan(emne_index, semester_nummer):
    # Gyldig tall i listen:
    if semester_nummer < 1 or semester_nummer > 6:
        print("Ugyldig nummer. Velg mellom 1-6")
        return 
    # Om emnet er ikke allerede lagt til:
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

    # Om det er plass i semesteret hvor maks poeng er 30 studiepoeng:
    naavaerende_sp = sum([studiepoeng[i] for i in studieplan[semester_nummer - 1]])
    if naavaerende_sp + studiepoeng[emne_index] > 30:
        print("Ikke plass til dette emnet i semesteret, maks 30 studiepoeng")
        return
    
    # Legg til emnet:
    studieplan[semester_nummer-1].append(emne_index)
    print(f"Emne {emnekoder[emne_index]} lagt till i semester {semester_nummer}")

# Oppgave 5
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

# Oppgave 6
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

