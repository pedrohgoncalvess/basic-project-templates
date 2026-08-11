## Universal architecture and general guidelines

This specification defines the universal architectural and implementation standards for software development. All applications, regardless of the programming language or framework used, must follow the same responsibilities, layer boundaries, naming standards, file size limits, and dependency directions.

Development must prioritize a function-based paradigm and modular composition over object-oriented structures with mutable state or complex inheritance.

---

## Directory structure and layers

Code organization must follow domain-driven design principles. Each domain groups its routes, contracts/models, services, and repositories.

Universal logical directory structure:

```text
application/
  core/
    config/
    database/
    exceptions/
    exception_handlers/
    logging/
  users/
    models/
    router/
    services/
    repository/
  orders/
    models/
    router/
    services/
    repository/
infrastructure/
  database/
  logging/
  migrations/
```

### Layer responsibilities

- **`router`**: Defines HTTP endpoints, validates request contracts, handles authentication/authorization, status codes, and response serialization. Must not contain SQL queries or business logic.
- **`services`**: Implements use cases and business logic. Coordinates repositories within the same unit of work and raises domain exceptions.
- **`repository`**: Handles domain-specific data persistence using the injected session or connection. Contains no business logic and never executes transaction commits (`commit`).
- **`models`**: Defines input (DTOs/schemas) and output API contracts, remaining separate from internal persistence models.
- **`core/database`**: Integration point that retrieves connections/sessions via Factory and manages resource lifecycles.
- **`core/exceptions`**: Declares generic domain errors independent of the HTTP protocol.
- **`core/exception_handlers`**: Global Exception Handler that intercepts exceptions and converts them into standardized HTTP responses.
- **`infrastructure`**: Contains concrete implementations for database access, drivers, logging clients, and external services.

Execution flow strictly follows this direction:

```text
Request -> Router -> Service -> Repository -> Database
                     |
                     -> Domain Exception -> Global Exception Handler -> Response
```

---

## Naming, formatting, and code size limits

Rules for naming, formatting, and file size apply equally across all programming languages:

### Naming conventions
- **Functions and variables**: Use `snake_case` with descriptive, action-oriented names (e.g., `calculate_order_total`, `find_user_by_public_id`).
- **Types, contracts, and schemas**: Use `PascalCase` (e.g., `UserCreateRequest`, `OrderSummary`).
- **Constants and enums**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_POOL_SIZE`, `DEFAULT_TIMEOUT`).
- **SQL tables, schemas, and columns**: Use `snake_case` explicitly enclosed in double quotes (e.g., `"communication"."message"`).

### Code and function standards
- **Function-based**: Write pure, modular functions wherever possible. Avoid static utility classes or mutable singletons.
- **File and module size**: Keep files small, cohesive, and focused on a single responsibility. The application entry point (composition root) must remain small, limited to registering routes, middlewares, and dependency injections.
- **Single Responsibility Principle (SRP)**: Each function must perform only one well-defined task and maintain a small line count.

---

## Database conventions

### 1. Connection factory pattern

Database connection creation must utilize the Factory pattern to decouple the application from specific drivers (PostgreSQL, MySQL, Oracle, Sybase) and execution modes (synchronous vs. asynchronous).

- Services and repositories must depend exclusively on an injected session/connection, without knowing driver details, connection string URLs, engine creation, or pool configurations.
- Implementations must be loaded **lazily**: only the provider and driver selected by configuration are imported and initialized at runtime.
- Configuration errors for unused providers must not prevent application startup.

### 2. Repository pattern and transactional boundaries

- The repository is the sole layer authorized to execute persistence queries for a domain.
- Repositories receive sessions via dependency injection and encapsulate queries, filters, and operations.
- Repositories must **never** execute `commit`.
- Intermediate state synchronizations must use `flush`.
- The **Session** represents the unit of work (transaction boundary):
  - Executes `commit` **once** when the complete service block succeeds.
  - Executes `rollback` whenever an exception escapes the execution flow.

### 3. Configuration and credentials

- Provider selection, host, port, database/service name, user, password, and pool limits must be read from environment variables.
- Validation must occur at application startup (fail-fast), halting startup if a required parameter is missing or invalid.
- Pool validation: minimum pool size must be greater than zero (`min_pool > 0`) and maximum pool size must be greater than or equal to the minimum (`max_pool >= min_pool`).
- **Development credentials**: Local PostgreSQL environments must default to user `postgres`, password `postgres`, and database `postgres`. Other engines must use their standard local development defaults.
- Real or production credentials must never appear in source code, repositories, or versioned Compose files.

### 4. Migrations, schemas, and SQL conventions

- Structural schema changes must be delivered exclusively via versioned migrations accompanied by rollback scripts.
- Irreversible operations must have their lack of rollback technically justified, documented, and approved prior to execution.
- **Mandatory domain schema**: All database objects (tables, functions, triggers, indexes) must belong to an explicit domain schema. Using the `public` schema is forbidden by default.
- **Double quote delimitation**: Schema and table names must always be enclosed in double quotes in migrations and manual SQL (format `"schema"."table"`).
- **Table definition structure**:
  1. Column declarations (name, type, nullability, default value).
  2. Table constraint declarations (Primary Key, Foreign Keys, Unique, Check) placed at the bottom of table definition.

### 5. SQL naming conventions

- **Primary key (PK)**: Follows the format `{table}_pk`. In case of schema collisions, use `{schema}_{table}_pk`.
- **Foreign key (FK)**: Follows the format `{main_table}_{foreign_table}_fk`. On collision, use `{schema}_{main_table}_{foreign_table}_fk`. For multiple FKs between the same tables, include a qualifier: `{main_table}_{qualifier}_{foreign_table}_fk`.
- **Constraints (UNIQUE/CHECK)**: Declared at the bottom of table definitions with explicit names.
- **Indexes**: Explicit names tied to schema and table (format `{schema}_{table}_{column}_idx`).
- **Column suffixes**:
  - Calendar dates: Suffix `_dt` and type `DATE` (e.g., `birth_dt`).
  - Timestamps / Date-Time: Suffix `_at` and type `TIMESTAMPTZ` (configured for timezone `America/Sao_Paulo`). Plain `TIMESTAMP` without timezone is forbidden.
  - Monetary values: Suffix `_vl` and type `DECIMAL(precision, 4)` (scale must strictly be `4`).
  - Quantities and counts: Suffix `_qt` (e.g., `item_qt`).
  - Encrypted or obfuscated fields: Must include an explicit database column comment:
    ```sql
    COMMENT ON COLUMN "schema"."table"."column_name" IS '[Encrypted] Field description';
    ```
  - Foreign key columns: Suffix `_id` prefixed by referenced table (e.g., `media_id`). Multiple FKs to the same table use qualifier prefixes (e.g., `received_media_id`, `sent_media_id`).

### 6. Dual identifiers for exposed tables

Every table exposed by the application must contain two identifiers:

1. **`id`**: Internal, sequential primary key (e.g., `BIGINT GENERATED ALWAYS AS IDENTITY`), used exclusively for internal relationships and transactions. Never exposed in external APIs.
2. **`public_id`**: Public, non-sequential identifier (UUID v4, e.g., `gen_random_uuid()`), exposed in external API contracts. Must have a `UNIQUE` constraint and index.

### 7. Universal SQL DDL example

```sql
CREATE SCHEMA IF NOT EXISTS "communication";

CREATE TABLE "communication"."message" (
    id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    public_id UUID NOT NULL DEFAULT gen_random_uuid(),
    customer_id BIGINT NOT NULL,
    received_media_id BIGINT,
    sent_media_id BIGINT,
    reference_dt DATE NOT NULL,
    amount_vl DECIMAL(18, 4) NOT NULL,
    attachment_qt INTEGER NOT NULL DEFAULT 0,
    received_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT message_pk
        PRIMARY KEY (id),
    CONSTRAINT communication_message_public_id_uk
        UNIQUE (public_id),
    CONSTRAINT message_customer_fk
        FOREIGN KEY (customer_id)
        REFERENCES "customer"."customer" (id),
    CONSTRAINT message_received_media_fk
        FOREIGN KEY (received_media_id)
        REFERENCES "media"."media" (id),
    CONSTRAINT message_sent_media_fk
        FOREIGN KEY (sent_media_id)
        REFERENCES "media"."media" (id),
    CONSTRAINT communication_message_attachment_qt_ck
        CHECK (attachment_qt >= 0),
    CONSTRAINT communication_message_amount_vl_ck
        CHECK (amount_vl >= 0),
    CONSTRAINT communication_message_status_ck
        CHECK (status IN ('pending', 'sent', 'failed'))
);

CREATE INDEX communication_message_customer_id_idx
    ON "communication"."message" (customer_id);

CREATE INDEX communication_message_received_at_idx
    ON "communication"."message" (received_at);
```

---

## Global exception handling and error formatting

All APIs must implement a Global Exception Handler as a single point of translation between application exceptions and standardized HTTP responses.

### Global Exception Handler rules
- Map domain exceptions to appropriate HTTP status codes.
- Hide internal details for unexpected failures (`500` status), returning generic messages without leaking stack traces, SQL queries, or credentials.
- Return a strictly standardized JSON payload:

```json
{
  "detail": "Email already registered.",
  "code": "EMAIL_ALREADY_REGISTERED",
  "correlation_id": "4c431bca-64dc-4fb7-9f42-b7f9499a2424"
}
```

- Preserve necessary response headers (e.g., `WWW-Authenticate`).
- Log errors in structured logs with the request correlation identifier (`correlation_id`).

---

## Structured logging and log factory

- **Factory pattern**: Logger instantiation must go through a Factory, allowing switching between synchronous and asynchronous loggers.
- **Structured format**: Logs must be output in JSON format including level (`INFO`, `WARN`, `ERROR`), timestamp, domain/module, event type, and details.
- **Correlation identifier**: All requests and background tasks must propagate a `correlation_id`.
- **Data protection**: Sensitive data such as passwords, tokens, secret keys, or unauthorized personal data must never be logged.
- **Exception logging**: Log errors where they are handled (preferably in the Global Exception Handler). Do not duplicate error logs across layers.

---

## Universal testing strategy

- **Unit tests**: Fast and deterministic. Must not access networks, external file systems, or real databases. Test Factories, business logic, and isolated validations using mocks at boundary interfaces.
- **API contract tests**: Validate endpoint integration starting from the application composition root, overriding infrastructure dependencies with controlled test mocks.
- **Integration tests**: Execute real operations against ephemeral containerized databases and services. Must remain disabled by default and require an explicit environment flag (`RUN_INTEGRATION_TESTS=true`).

---

## Packaging and execution with Docker

- **Docker Compose**: Standard tool to manage container build, configuration, and lifecycle in development and execution environments.
- **Lean images**: Use multi-stage builds and official base images with pinned version tags (using `latest` is forbidden).
- **Security**: Run containers as non-root users. Never embed secret files or credentials into image build contexts.