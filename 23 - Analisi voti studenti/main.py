def extract_grade(student):
    parts = student.split()
    return int(parts[1]) if len(parts) == 2 else None

student_grades = {}


total_sum = 0
total_count = 0
highest_grade = 0
highest_students = []

with open("studenti.txt", "r") as source:
    for line in source:
        line = line.strip()
        
        grade = extract_grade(line)
        
        if grade is not None:
            total_sum += grade
            total_count += 1
            
            if grade > highest_grade:
                highest_grade = grade
                highest_students = [line.split()[0]]
            elif grade == highest_grade:
                highest_students.append(line.split()[0])            
            
            if grade not in student_grades:
                student_grades[grade] = []
            student_grades[grade].append(line.split()[0])

# Calcola la media dei voti
average_grade = total_sum / total_count if total_count > 0 else 0

# Stampa i risultati
print(f"Media dei voti: {average_grade:.2f}")
print(f"Voto più alto: {highest_grade}")
print(f"Studenti con il voto più alto: {', '.join(highest_students)}")

# Stampa il dizionario che raggruppa gli studenti per voto
print("\nDizionario degli studenti per voto:")
for grade, students in student_grades.items():
    print(f"Voto {grade}: {', '.join(students)}")
