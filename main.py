# import
import csv
import sys
import os

# import pandas
import quopri
import pandas as pd
import geo_coding
import osm
import website

# variablen daklaration

Kontakt_new = []
Kontakt = []
kontakte_daten = []
csv_file = os.path.abspath(".") + "/Kontakte.csv"
vcf_file = os.path.abspath(".") + "/2022-10-06_151740.vcf"
# df_Kontakte_old = pd.read_csv(csv_file)

print("Programm start")
# _______________decodiert die Verschlüsstelten Adress Daten aus dem vcf File
def decode_adr(vcf_data_list, i):
    # print('dekodiere adresse')
    if (
        vcf_data_list[i + 1][0] == "="
    ):  # prüft ob die Codierte message über mehrere Zeilen geht
        # geht die Codierte Adresse über mehrere Zeilen
        # werden diese in eine Variablen zusammengefasst um diese dann zu Decodieren
        print("mehrere zeilen")
        adress_data = vcf_data_list[i].split(":")[1] + vcf_data_list[i + 1][1:]
        adress = decode_QP(adress_data)
    else:
        adress = decode_QP(vcf_data_list[i].split(":")[1])
    # print(adress)
    return adress


# __________________________________________decodiert den QP code und gibt diesen als String zurück____________________
def decode_QP(str_verschlüsselt):
    temp3 = quopri.decodestring(str_verschlüsselt)
    temp3 = temp3.decode("utf-8")
    temp3 = temp3.split(";")[2]
    return temp3


# ________________________________________liest die Kontaktdatei vom Handy aus______________________
def vcf_read():
    data = {
        "Name": [None],
        "Tel": [None],
        "Street": [None],
        "Hausnummer": [None],
        "Ort": [None],
        "Plz": [None],
    }
    dfKontakte = pd.read_csv(csv_file)
    # print(dfKontakte)
    with open(vcf_file, mode="r") as vcf:  # öffnet die vcf datei mit den Kontakte
        vcf_data = vcf.read()  # liest vcf file aus
        vcf_data_list = vcf_data.splitlines()  # trennt ausgelesenden file nach zeilen
        i = 0
        adresse = []
        while i + 1 < len(vcf_data_list):  # durchläuft einmal ganze liste
            name = "s"
            # tel='s'
            try:

                if (
                    vcf_data_list[i][0] + (vcf_data_list[i][1]) + (vcf_data_list[i][2])
                ) == "ADR":  # sucht Positionen die mit ADR beginnen in Liste (Zeichen für Adresse)
                    if "QUOTED-PRINTABLE" in vcf_data_list[i]:
                        # print(i)
                        adresse.append(decode_adr(vcf_data_list, i))
                    # Kontakt_new.append(tempkontakt)
                    else:
                        adresse.append(vcf_data_list[i].split(";")[3])
                    # print(i)
                    # print(len(adresse))
                    if len(adresse) == 2:

                        x = i
                        while not vcf_data_list[x][:3] in "TEL":
                            x = x - 1
                        tel = vcf_data_list[x].split(":")[1]
                        name = vcf_data_list[x - 1].split(":")[1]
                        ort = adresse[1].split(" ")
                        straße_l = adresse[0].split(" ")
                        street_name = ""
                        Ort_name = ""
                        for t in ort:
                            if t.isdigit():
                                plz = t
                            else:
                                Ort_name = Ort_name + " " + t
                        for t in straße_l:
                            if t.isdigit():
                                hausnummer_i = t
                            else:
                                street_name = street_name + " " + t
                        data = {
                            "Name": [name],
                            "Tel": [tel],
                            "Street": [street_name],
                            "Hausnummer": [hausnummer_i],
                            "Ort": [Ort_name],
                            "Plz": [plz],
                        }
                        # print(name)
                        new = kontakt_new_test(name, dfKontakte)
                        if new:
                            print("neuer Kontakt gefunden")
                            df2 = pd.DataFrame(data)
                            #   print(df2)
                            dfKontakte = dfKontakte.append(df2)
                        # print(dfKontakte)
                        adresse = []
            except Exception as e:
                print(e)
                # print(name)
                # print('df2')
            i = i + 1
    dfKontakte.to_csv(csv_file, index=False)
    return dfKontakte
    x = 0


def kontakt_new_test(name, df_Kontakte):
    # kontrolliert ob der neue Kontakt bereits vorhanden ist und
    # gibt dementsprechend True oder False zurück
    kontakt_vorhanden = False
    for i, row in df_Kontakte.iterrows():
        # print(row)
        if row.get("Name") == name:
            print("der Kontakt ist bereits vorhanden")
            kontakt_vorhanden = True
    if not kontakt_vorhanden:
        print("neuen Kontakt speichern")
        return True
    else:
        return False


# _____________fals noch keine csv vorhanden ist wird diese Hier erstellt
# prüfung ob vorhanden in in arbeit
def create_new_csv():
    print("create new csv")
    with open(csv_file, "w", encoding="utf-8") as csv_datei:
        writer = csv.writer(csv_datei, delimiter=",")
        writer.writerow(["Name", "Nummer", "Straße", "Hausnummer", "Ort", "Plz"])


def loade_csv():
    print("loade csv")
    return pd.read_csv("Kontakte.csv")


def main(search_parameter):
    # create_new_csv()
    # dfkontakte = vcf_read()
    dfkontakte = loade_csv()
    osm_ids_kontakte,kontakte_daten = geo_coding.get_osm_id(dfkontakte)
    results = osm.osm_main(osm_ids_kontakte)
    #osm.print_per_uid_ptty(osm_ids_kontakte,results)
    website.show_at_map(osm_ids_kontakte,results,kontakte_daten)
    # osm.print_per_uid_ptty(osm_ids_kontakte, name=False)



