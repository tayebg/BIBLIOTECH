import { useState, useEffect } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

export interface Book {
  id: string;
  authorId: string;
  authorFirstName: string;
  authorLastName: string;
  isbn: string;
  title: string;
  year: number;
  created_at?: string;
  updated_at?: string;
}

export const useBooks = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();

  const fetchBooks = async () => {
    try {
      const { data, error } = await supabase
        .from('books')
        .select(`
          *,
          authors (
            id,
            first_name,
            last_name
          )
        `)
        .order('title', { ascending: true });

      if (error) throw error;

      const mappedBooks = data.map(book => ({
        id: book.id,
        authorId: book.author_id,
        authorFirstName: book.authors.first_name,
        authorLastName: book.authors.last_name,
        isbn: book.isbn,
        title: book.title,
        year: book.year,
        created_at: book.created_at,
        updated_at: book.updated_at
      }));

      setBooks(mappedBooks);
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error fetching books",
        description: error.message,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const addBook = async (authorId: string, isbn: string, title: string, year: number) => {
    try {
      const { data, error } = await supabase
        .from('books')
        .insert([{ 
          author_id: authorId, 
          isbn: isbn, 
          title: title, 
          year: year 
        }])
        .select(`
          *,
          authors (
            id,
            first_name,
            last_name
          )
        `)
        .single();

      if (error) throw error;

      const newBook = {
        id: data.id,
        authorId: data.author_id,
        authorFirstName: data.authors.first_name,
        authorLastName: data.authors.last_name,
        isbn: data.isbn,
        title: data.title,
        year: data.year,
        created_at: data.created_at,
        updated_at: data.updated_at
      };

      setBooks(prev => [...prev, newBook]);
      
      toast({
        title: "Book added",
        description: `"${title}" has been added successfully.`,
      });

      return { success: true };
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error adding book",
        description: error.message,
      });
      return { success: false, error: error.message };
    }
  };

  const updateBook = async (id: string, authorId: string, isbn: string, title: string, year: number) => {
    try {
      const { data, error } = await supabase
        .from('books')
        .update({ 
          author_id: authorId, 
          isbn: isbn, 
          title: title, 
          year: year 
        })
        .eq('id', id)
        .select(`
          *,
          authors (
            id,
            first_name,
            last_name
          )
        `)
        .single();

      if (error) throw error;

      const updatedBook = {
        id: data.id,
        authorId: data.author_id,
        authorFirstName: data.authors.first_name,
        authorLastName: data.authors.last_name,
        isbn: data.isbn,
        title: data.title,
        year: data.year,
        created_at: data.created_at,
        updated_at: data.updated_at
      };

      setBooks(prev => 
        prev.map(book => book.id === id ? updatedBook : book)
      );

      toast({
        title: "Book updated",
        description: `"${title}" has been updated successfully.`,
      });

      return { success: true };
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error updating book",
        description: error.message,
      });
      return { success: false, error: error.message };
    }
  };

  const deleteBook = async (id: string) => {
    try {
      const { error } = await supabase
        .from('books')
        .delete()
        .eq('id', id);

      if (error) throw error;

      setBooks(prev => prev.filter(book => book.id !== id));
      
      toast({
        title: "Book deleted",
        description: "Book has been deleted successfully.",
      });

      return { success: true };
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error deleting book",
        description: error.message,
      });
      return { success: false, error: error.message };
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return {
    books,
    isLoading,
    addBook,
    updateBook,
    deleteBook,
    refetch: fetchBooks
  };
};