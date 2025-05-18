CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE admins (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR,
    "password" VARCHAR
);

INSERT INTO admins(name, password) VALUES ('admin', ENCODE(DIGEST('123456', 'sha256'), 'hex'));

CREATE TABLE "products" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
    "product_code" bigint,
  "description" text,
  "manufacturer_id" integer,
  "category_id" integer,
  "image_filename" varchar
);

CREATE TABLE "categories" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar unique
);

CREATE TABLE "manufacturers" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar unique,
  "image_filename" varchar
);

CREATE TABLE "price_changes" (
  "id" SERIAL PRIMARY KEY,
  "date" timestamp default current_timestamp,
  "product_id" integer,
  "price" integer
);

CREATE TABLE "deliveries" (
  "id" SERIAL PRIMARY KEY,
  "product_id" integer,
  "count" integer,
  "date" timestamp default current_timestamp
);

CREATE TABLE "sales" (
  "id" SERIAL PRIMARY KEY,
  "order_id" integer,
  "product_id" integer,
  "count" integer
);

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar unique,
  "phone_number" varchar,
  "password" varchar,
  "registration_date" timestamp DEFAULT current_timestamp
);

CREATE TABLE "orders" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer,
  "date" timestamp DEFAULT current_timestamp,
  "address" varchar
);

CREATE TABLE "order_statuses" (
  "id" SERIAL PRIMARY KEY,
  "order_id" integer,
  "status" integer default 1,
  "date" timestamp DEFAULT current_timestamp
);

CREATE TABLE "warehouse" (
  "product_id" SERIAL PRIMARY KEY,
  "count" integer
);

CREATE TABLE "carts" (
  "id" SERIAL PRIMARY KEY,
  "product_id" integer,
  "user_id" integer,
  "count" integer,
  "added_at" timestamp DEFAULT current_timestamp
);

CREATE TABLE "new_collection" (
  "id" SERIAL PRIMARY KEY,
  "product_id" integer unique
);

ALTER TABLE "products" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON DELETE CASCADE;

ALTER TABLE "new_collection" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE;

ALTER TABLE "price_changes" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE;

ALTER TABLE "deliveries" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE;

ALTER TABLE "sales" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE;

ALTER TABLE "sales" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "order_statuses" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");

ALTER TABLE "carts" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE;

ALTER TABLE "carts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE carts ADD CONSTRAINT unique_product_client UNIQUE (product_id, user_id);
