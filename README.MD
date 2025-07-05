# Book Management System ERD

## MODELS

```mermaid
erDiagram
%% ====================================================
%% TURIVIUS - BOOK MANAGEMENT SYSTEM ERD
%% INDEXED FIELDS: books.title, books.isbn_code, authors.name, book_data.title, language, all FKs
%% SHARDING: branch_id used in physical_exemplars and book_lending
%% ====================================================


    %% RELATIONSHIPS
    authors ||--o{ authors_books : has
    books ||--o{ authors_books : has

    books ||--o{ category_books : categorized
    book_categories ||--o{ category_books : contains

    books ||--o{ physical_exemplars : has
    branches ||--o{ physical_exemplars : stores

    books ||--o{ book_data : has_translations

    user_types ||--o{ users : defines
    users ||--o{ book_lending : lends
    physical_exemplars ||--o{ book_lending : lent
    branches ||--o{ book_lending : in

    %% ENTITIES

    authors {
        uuid id PK
        string name
        datetime created_at
        string created_by
        datetime updated_at
        string updated_by
    }

    books {
        uuid id PK
        string title
        string isbn_code
        string editor
        int edition
        string type
        datetime publish_date
        datetime created_at
        string created_by
        datetime updated_at
        string updated_by
    }

    authors_books {
        uuid author_id FK
        uuid book_id FK
        datetime created_at
        string created_by
    }

    book_categories {
        uuid id PK
        string name
        string description
        datetime created_at
        string created_by
        datetime updated_at
        string updated_by
    }

    category_books {
        uuid book_category_id FK
        uuid book_id FK
        datetime created_at
        string created_by
    }

    branches {
        uuid id PK
        string name
    }

    physical_exemplars {
        uuid id PK
        boolean available
        uuid book_id FK
        uuid branch_id FK
        int room
        int floor
        int bookshelf
    }

    book_data {
        uuid id PK
        uuid book_id FK
        string language
        string summary
        string title
        datetime created_at
        string created_by
        datetime updated_at
        string updated_by
    }

    users {
        uuid id PK
        string name
        uuid type_id FK
    }

    user_types {
        uuid id PK
        string type
        int max_books
    }

    book_lending {
        uuid id PK
        uuid physical_book_id FK
        uuid lend_by FK
        uuid branch_id FK
        datetime reserved_at
        datetime lend_at
        datetime returned_at
        datetime planned_returned_at
    }
