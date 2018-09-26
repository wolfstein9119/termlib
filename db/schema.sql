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
-- Триггер на подготовку данных при изменении таблицы term
------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.prepare_term() RETURNS trigger AS $prepare_term$
BEGIN
    NEW.name = TRIM(NEW.name);
    NEW.name = REGEXP_REPLACE(NEW.name, '\s+', ' ', 'g');

    IF LENGTH(NEW.name) < 1 THEN
        RAISE EXCEPTION 'column name in public.term must contain symbol';
    END IF;

    NEW.name = UPPER(SUBSTR(NEW.name, 1, 1)) || SUBSTR(NEW.name, 2);

    RETURN NEW;
END;

$prepare_term$ LANGUAGE plpgsql;

CREATE TRIGGER prepare_term BEFORE INSERT OR UPDATE ON public.term
    FOR EACH ROW EXECUTE PROCEDURE public.prepare_term();
