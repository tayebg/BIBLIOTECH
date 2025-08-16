-- Allow anonymous users to perform all operations on authors table
-- Run these commands in your Supabase SQL Editor

-- Enable RLS on authors table (if not already enabled)
ALTER TABLE public.authors ENABLE ROW LEVEL SECURITY;

-- Allow anonymous users to select authors
CREATE POLICY "authors_select_anon" ON public.authors 
FOR SELECT TO anon 
USING (true);

-- Allow anonymous users to insert authors
CREATE POLICY "authors_insert_anon" ON public.authors 
FOR INSERT TO anon 
WITH CHECK (true);

-- Allow anonymous users to update authors
CREATE POLICY "authors_update_anon" ON public.authors 
FOR UPDATE TO anon 
USING (true) 
WITH CHECK (true);

-- Allow anonymous users to delete authors
CREATE POLICY "authors_delete_anon" ON public.authors 
FOR DELETE TO anon 
USING (true);

-- Do the same for books table if needed
ALTER TABLE public.books ENABLE ROW LEVEL SECURITY;

CREATE POLICY "books_select_anon" ON public.books 
FOR SELECT TO anon 
USING (true);

CREATE POLICY "books_insert_anon" ON public.books 
FOR INSERT TO anon 
WITH CHECK (true);

CREATE POLICY "books_update_anon" ON public.books 
FOR UPDATE TO anon 
USING (true) 
WITH CHECK (true);

CREATE POLICY "books_delete_anon" ON public.books 
FOR DELETE TO anon 
USING (true);