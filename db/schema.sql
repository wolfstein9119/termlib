------------------------------------------------------------------------------------------------------------------------
-- Таблица понятий
------------------------------------------------------------------------------------------------------------------------
CREATE TABLE public.term (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);

CREATE SEQUENCE public.term_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.term_id_seq OWNED BY public.term.id;

ALTER TABLE ONLY public.term ALTER COLUMN id SET DEFAULT nextval('public.term_id_seq'::regclass);

ALTER TABLE ONLY public.term
    ADD CONSTRAINT term_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.term
    ADD CONSTRAINT term_name_key UNIQUE (name);

------------------------------------------------------------------------------------------------------------------------
-- Таблица определений
------------------------------------------------------------------------------------------------------------------------
CREATE TABLE public.definition (
    id integer NOT NULL,
    term_id integer NOT NULL,
    priority integer DEFAULT 0 NOT NULL,
    text text NOT NULL
);

CREATE SEQUENCE public.definition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.definition_id_seq OWNED BY public.definition.id;

ALTER TABLE ONLY public.definition ALTER COLUMN id SET DEFAULT nextval('public.definition_id_seq'::regclass);

ALTER TABLE ONLY public.definition
    ADD CONSTRAINT definition_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.definition
    ADD CONSTRAINT term_id_priority UNIQUE (term_id, priority);

ALTER TABLE ONLY public.definition
    ADD CONSTRAINT definition_term_id_fkey FOREIGN KEY (term_id) REFERENCES public.term(id);

------------------------------------------------------------------------------------------------------------------------
-- Общие функции
------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.normalize_string(in_str VARCHAR, empty_error_msg VARCHAR) RETURNS varchar AS $normalize_string$
DECLARE
    result VARCHAR;
BEGIN
    result = TRIM(in_str);
    result = REGEXP_REPLACE(result, '\s+', ' ', 'g');

    IF LENGTH(result) < 1 THEN
        RAISE EXCEPTION '%', empty_error_msg;
    END IF;

    RETURN result;
END;

$normalize_string$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------------------------------------------
-- Триггер на подготовку данных при изменении таблицы term
------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.prepare_term() RETURNS trigger AS $prepare_term$
BEGIN
    NEW.name = normalize_string(NEW.name, 'column name in public.term must contain symbol');
    NEW.name = UPPER(SUBSTR(NEW.name, 1, 1)) || SUBSTR(NEW.name, 2);
    RETURN NEW;
END;

$prepare_term$ LANGUAGE plpgsql;

CREATE TRIGGER prepare_term BEFORE INSERT OR UPDATE ON public.term
    FOR EACH ROW EXECUTE PROCEDURE public.prepare_term();

------------------------------------------------------------------------------------------------------------------------
-- Триггер на подготовку данных при изменении таблицы definition
------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.prepare_definition() RETURNS trigger AS $prepare_definition$
BEGIN
    NEW.text = normalize_string(NEW.text, 'column text in public.definition must contain symbol');
    RETURN NEW;
END;

$prepare_definition$ LANGUAGE plpgsql;

CREATE TRIGGER prepare_definition BEFORE INSERT OR UPDATE ON public.definition
    FOR EACH ROW EXECUTE PROCEDURE public.prepare_definition();

------------------------------------------------------------------------------------------------------------------------
-- Вьюха для представления понятий
------------------------------------------------------------------------------------------------------------------------
CREATE VIEW public.terms_with_definitions
  AS
    SELECT t.id, t.name, ARRAY_AGG(d.text) as definitions
    FROM public.term as t
    JOIN public.definition as d ON t.id = d.term_id
    GROUP BY t.id, t.name;
