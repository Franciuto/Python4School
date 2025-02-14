from datetime import date

annoNascita = int(input("Inserisci anno di nascita: "))
meseNascita = int(input("Inserisci mese: "))
giornoNascita = int(input("Inserisci giorno: "))

oggi = date.today()


anno = oggi.year
mese = oggi.month
giorno = oggi.day

if (mese > meseNascita or (mese == meseNascita and giorno >= giornoNascita)):
    età = anno - annoNascita
else:
    età = anno - annoNascita - 1

print(f'Hai {età} anni')
