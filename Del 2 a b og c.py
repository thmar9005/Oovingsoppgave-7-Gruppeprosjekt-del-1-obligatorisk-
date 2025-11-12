import json  # brukes til å lagre og lese data til en JSON fil senere i koden

# Representerer ett fag (emne) med kode, navn, semester og studiepoeng.
# Har en metode for å gjøre data klar til å lagres i en JSON fil i tilleg.
class Emne:
    def __init__(self, kode, navn, semester, studiepoeng, eksamensform=None, beskrivelse=None):
        self.kode = kode
        self.navn = navn
        self.semester = semester.upper()  # .upper() gjør input til stor bokstav
        self.studiepoeng = studiepoeng
        self.eksamensform = eksamensform
        self.beskrivelse = beskrivelse

    def __str__(self):
        sem_full = "høst" if self.semester == "H" else "vår"
        return f"{self.kode} - {self.navn} ({sem_full}), {self.studiepoeng} studiepoeng."


    def to_dict(self):
        """Gjør Emne-objektet om til en enkel ordbok (for JSON-lagring)."""
        #gjør emnet om til dict dom kan lagres i JSON
        return {
            "kode": self.kode,
            "navn": self.navn,
            "semester": self.semester,
            "studiepoeng": self.studiepoeng,
            "eksamensform": self.eksamensform,
            "beskrivelse": self.beskrivelse,
        }

# Representerer en hel studieplan (1–6 semestre).
# Kan legge til emner, skrive ut planen, sjekke gyldighet og lagre som JSON.
class Studieplan:
    def __init__(self, plan_id, tittel):
        self.plan_id = plan_id
        self.tittel = tittel
        self.semestre = [[] for _ in range(6)]  # liste med 6 semestre

    def legg_til_emne(self, emne, semester_nummer: int):
        # Passer på at semester er mellom 1 og 6
        if semester_nummer < 1 or semester_nummer > 6:
            print("Ugyldig nummer. Velg mellom 1-6")
            return

        # Sjekker om den allerede eksisterer og hinderer kopier av emner
        for sem in self.semestre:
            if emne in sem:
                print("Dette emnet finnes allerede i denne studieplanen.")
                return

        # Gjør at høstsemester emner ikke kan bli lagt til i vår semester og motsatt
        if emne.semester == "H" and semester_nummer % 2 == 0:
            print("Dette er et høstemne og kan ikke legges til i et vårsemester.")
            return
        if emne.semester == "V" and semester_nummer % 2 == 1:
            print("Dette er et våremne og kan ikke legges til i et høstsemester.")
            return

        # Sjekk 30 sp-grense
        nåværende_sp = sum(e.studiepoeng for e in self.semestre[semester_nummer - 1])
        if nåværende_sp + emne.studiepoeng > 30:
            print("Ikke plass til dette emnet i semesteret, maks 30 studiepoeng.")
            return

        # Legger til emnet
        self.semestre[semester_nummer - 1].append(emne)
        print(f"Emne {emne.kode} lagt til i semester {semester_nummer} i '{self.tittel}'")

    def skriv_ut(self):
        # Viser alle semestre og emner i planen på en ryddig måte.
        print(f"\n--- Studieplan: {self.tittel} (ID: {self.plan_id}) ---")
        for i, sem in enumerate(self.semestre, start=1):
            if not sem:
                print(f"Semester {i}: (ingen emner)")
            else:
                total_sp = sum(e.studiepoeng for e in sem)
                print(f"Semester {i}:")
                for e in sem:
                    sem_full = "høst" if e.semester == "H" else "vår"
                    print(f"  {e.kode} - {e.navn} ({sem_full}), {e.studiepoeng} studiepoeng")
                print(f"  Totalt: {total_sp} studiepoeng\n")

    def sjekk_gyldighet(self):
        # Sjekker om hvert semester har nøyaktig 30 studiepoeng.
        gyldig = True
        for i, sem in enumerate(self.semestre, start=1):
            total_sp = sum(e.studiepoeng for e in sem)
            if total_sp != 30:
                print(f"Semester {i}: {total_sp} sp -> ikke gyldig (må være 30 sp)")
                gyldig = False
            else:
                print(f"Semester {i}: 30 sp")
        if gyldig:
            print("Hele studieplanen er gyldig.")
        else:
            print("Studieplanen er ikke gyldig (se detaljer over).")

    def to_dict(self):
        # Gjør hele studieplanen klar til å lagres som JSON.
        return {
            "plan_id": self.plan_id,
            "tittel": self.tittel,
            "semestre": [[e.to_dict() for e in sem] for sem in self.semestre],
        }

    def lagre_json(self, path="studieplan.json"):
        # Lagrer denne planen som en JSON-fil.
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
        print(f"Studieplan '{self.tittel}' lagret til '{path}'")



# Eksterne funksjoner for JSON
# Disse to ligger utenfor klassen
def fra_dict(data, emneregister):
    # Bygger en Studieplan fra dict (typisk fra JSON)
    ny = Studieplan(data["plan_id"], data["tittel"])
    for i, sem in enumerate(data.get("semestre", [])):
        for e in sem:
            # Bruker eksisterende emne hvis det allerede finnes i registeret
            emne = next((x for x in emneregister if x.kode == e["kode"]), None)
            if emne is None:
                emne = Emne(
                    e["kode"],
                    e.get("navn", ""),
                    e.get("semester", "H"),
                    e.get("studiepoeng", 0),
                    e.get("eksamensform"),
                    e.get("beskrivelse"),
                )
                emneregister.append(emne)
            ny.semestre[i].append(emne)
    return ny


def les_json(path, emneregister):
    # Leser en studieplan fra JSON og returnerer et Studieplan-objekt.
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        ny = fra_dict(data, emneregister)
        print(f"Studieplan '{ny.tittel}' lastet fra '{path}'")
        return ny
    except FileNotFoundError:
        print(f"Fant ikke filen '{path}'. Sørg for at den er lagret først.")
    except Exception as e:
        print(f"En feil oppstod under lesing: {e}")
    return None


# Her lagres alle emner, alle planer og ID-en til den aktive planen.
emner = []
studieplaner = []
aktiv_plan_id = None


# Funksjoner som brukes i menyen
def lag_nytt_emne(kode, navn, semester, studiepoeng, eksamensform=None, beskrivelse=None):
    # Legger til et nytt emne i emneregisteret.
    if any(e.kode == kode for e in emner):
        print("Et emne med denne koden finnes allerede.")
        return
    nytt_emne = Emne(kode, navn, semester, studiepoeng, eksamensform, beskrivelse)
    emner.append(nytt_emne)
    print(f"Emnet '{kode}' lagt til med {studiepoeng} studiepoeng.")

def skriv_ut_alle_emner():
    # Viser alle registrerte emner.
    if not emner:
        print("Ingen emner er registrert ennå.")
        return
    print("\n--- Alle registrerte emner ---")
    for i, e in enumerate(emner):
        print(f"[{i}] {e}")

def finn_plan_med_id(pid):
    # Finner en plan basert på ID.
    return next((p for p in studieplaner if p.plan_id == pid), None)

def skriv_ut_alle_studieplaner():
    # Lister alle opprettede planer og markerer hvilken som er aktiv.
    if not studieplaner:
        print("Ingen studieplaner er opprettet ennå.")
        return
    print("\n--- Alle studieplaner ---")
    for p in studieplaner:
        mark = " (AKTIV)" if aktiv_plan_id == p.plan_id else ""
        print(f"ID {p.plan_id}: {p.tittel}{mark}")

def krever_aktiv_plan():
    # Henter den aktive studieplanen, eller advarer hvis ingen er valgt.
    global aktiv_plan_id
    if aktiv_plan_id is None:
        print("Ingen aktiv studieplan. Velg eller opprett en plan først (valg 1 eller 2).")
        return None
    plan = finn_plan_med_id(aktiv_plan_id)
    if plan is None:
        print("Fant ikke aktiv studieplan.")
    return plan



# Dette er programloopen som kjøres i terminalen.
def hovedmeny():
    global aktiv_plan_id

    while True:
        print("\n--- STUDIEPLAN MENY ---")
        print("1. Opprett ny studieplan")
        print("2. Velg aktiv studieplan")
        print("3. Legg til et nytt emne i emneregisteret")
        print("4. Legg til et emne i AKTIV studieplan")
        print("5. Skriv ut alle registrerte emner")
        print("6. Skriv ut AKTIV studieplan")
        print("7. Sjekk gyldighet for AKTIV studieplan")
        print("8. Skriv AKTIV studieplan til en JSON fil")
        print("9. Les studieplan fra JSON som en NY plan")
        print("10. Vis alle studieplaner")
        print("11. Avslutt")

        valg = input("Velg et tall: ").strip()

        # Oppretter en studieplan
        if valg == "1":
            pid = int(input("Ny plan-ID (heltall): ").strip())
            if finn_plan_med_id(pid):
                print("En plan med denne ID-en finnes allerede.")
                continue
            tittel = input("Tittel på studieplan: ").strip()
            ny = Studieplan(pid, tittel)
            studieplaner.append(ny)
            aktiv_plan_id = pid
            print(f"Laget ny plan '{tittel}' (ID {pid}) og satt den som AKTIV.")

        # Velger vilken studieplan som er aktiv
        elif valg == "2":
            skriv_ut_alle_studieplaner()
            pid = int(input("Skriv inn ID på planen du vil aktivere: ").strip())
            if finn_plan_med_id(pid):
                aktiv_plan_id = pid
                print(f"Aktiv studieplan satt til ID {pid}.")
            else:
                print("Fant ikke plan med den ID-en.")

        # Legger til nytt emne
        elif valg == "3":
            kode = input("Emnekode: ").strip()
            navn = input("Navn: ").strip()
            sem = input("Semester (H/V): ").strip().upper()
            sp = int(input("Studiepoeng: ").strip())
            lag_nytt_emne(kode, navn, sem, sp)

        # Legger til emne i aktiv plan
        elif valg == "4":
            plan = krever_aktiv_plan()
            if plan is None:
                continue
            skriv_ut_alle_emner()
            emne_index = int(input("Emneindeks (starter på 0): ").strip())
            semester_nummer = int(input("Semester (1-6): ").strip())
            if 0 <= emne_index < len(emner):
                plan.legg_til_emne(emner[emne_index], semester_nummer)
            else:
                print("Ugyldig emneindeks.")

        # Viser alle emner
        elif valg == "5":
            skriv_ut_alle_emner()

        # Skriver ut aktiv plan
        elif valg == "6":
            plan = krever_aktiv_plan()
            if plan:
                plan.skriv_ut()

        # Sjekker gyldighet for aktiv studieplan
        elif valg == "7":
            plan = krever_aktiv_plan()
            if plan:
                plan.sjekk_gyldighet()

        # Lagrer til JSON
        elif valg == "8":
            plan = krever_aktiv_plan()
            if plan:
                path = input("Filnavn (default 'studieplan.json'): ").strip() or "studieplan.json"
                plan.lagre_json(path)

        # Les fra JSON
        elif valg == "9":
            pid = int(input("Ny plan-ID for innlest plan: ").strip())
            if finn_plan_med_id(pid):
                print("Det finnes allerede en plan med denne ID-en.")
                continue
            tittel = input("Tittel for innlest plan: ").strip()
            path = input("Filnavn å lese (default 'studieplan.json'): ").strip() or "studieplan.json"
            ny = les_json(path, emner)
            if ny:
                ny.plan_id = pid
                ny.tittel = tittel
                studieplaner.append(ny)
                aktiv_plan_id = pid
                print(f"Plan '{tittel}' (ID {pid}) er nå AKTIV (fra '{path}').")

        # Viser alle planer
        elif valg == "10":
            skriv_ut_alle_studieplaner()

        # Avslutter programmet
        elif valg == "11":
            print("Avslutter programmet.")
            break

        else:
            print("Ugyldig valg, prøv igjen.")


# Denne delen sørger for at menyen bare starter hvis filen kjøres direkte.
if __name__ == "__main__":
    hovedmeny()
