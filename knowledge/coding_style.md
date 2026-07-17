# Coding Style & Architecture - Johan (Bos)

## Tentang Bos
- Nama: Johan Erlangga
- Role: Flutter Developer di Unipos
- Tech stack utama: Flutter/Dart, Laravel, Python, Firebase

## Flutter - Atomic Design Structure
lib/
├── core/
│   ├── constants/
│   ├── theme/
│   └── utils/
├── components/
│   ├── atoms/         # Widget terkecil: Button, Text, Input
│   ├── molecules/     # Gabungan atoms: FormField, CardItem  
│   ├── organisms/     # Gabungan molecules: Header, ProductList
│   └── templates/     # Layout halaman
├── features/
│   └── feature_name/
│       ├── data/
│       │   ├── models/
│       │   └── repositories/
│       ├── domain/
│       │   └── entities/
│       └── presentation/
│           ├── pages/
│           ├── widgets/
│           └── providers/

## State Management
- Gunakan Riverpod untuk project baru
- GetX untuk project yang udah jalan
- Hindari setState kecuali untuk widget lokal sederhana

## Naming Convention
- File: snake_case → product_card.dart
- Class: PascalCase → ProductCard
- Variable: camelCase → productName
- Constant: kCamelCase → kPrimaryColor
- Widget atom suffix → ButtonAtom, TextAtom
- Widget molecule suffix → ProductCardMolecule
- Widget organism suffix → ProductListOrganism

## API Integration
- Gunakan Dio untuk HTTP client
- Setiap response punya model class sendiri
- Wajib error handling di setiap API call
- Base URL disimpen di constants

## Database
- Firebase Firestore untuk realtime
- SQLite untuk local storage
- Hive untuk simple key-value storage

## Code Style
- Maksimal 300 baris per file
- Selalu pisah logic dari UI
- Gunakan extension methods untuk utility
- Wajib dartdoc comment untuk public methods

## Laravel - Structure
app/
├── Http/
│   ├── Controllers/
│   ├── Middleware/
│   └── Requests/
├── Models/
├── Services/
└── Repositories/

## Prinsip Utama
- Clean code di atas segalanya
- Jangan hardcode, selalu gunakan constants
- Setiap function satu tanggung jawab (SRP)
- Selalu validasi input dari user