import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Edit, Trash2, ChevronUp, ChevronDown } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useBooks, Book } from '@/hooks/useBooks';
import { useAuthors } from '@/hooks/useAuthors';

export const LivresPage = () => {
  const { toast } = useToast();
  const { books, isLoading: booksLoading, addBook, updateBook, deleteBook } = useBooks();
  const { authors, isLoading: authorsLoading } = useAuthors();

  // Form state
  const [newBook, setNewBook] = useState({
    authorId: '',
    isbn: '',
    title: '',
    year: ''
  });

  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);

  // Edit state
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({
    authorId: '',
    isbn: '',
    title: '',
    year: ''
  });
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  // Sorting state
  const [sortField, setSortField] = useState<'title' | 'authorLastName' | 'isbn' | 'year'>('title');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Update filtered books when books or search changes
  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredBooks(books);
    } else {
      const filtered = books.filter(book => 
        book.authorLastName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.authorFirstName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.isbn.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.year.toString().includes(searchQuery)
      );
      setFilteredBooks(filtered);
    }
    setCurrentPage(1);
  }, [books, searchQuery]);

  const handleAddBook = async () => {
    if (!newBook.authorId || !newBook.isbn.trim() || !newBook.title.trim() || !newBook.year.trim()) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive"
      });
      return;
    }

    // Validate year (must be numeric and 4 digits)
    const yearRegex = /^\d{4}$/;
    if (!yearRegex.test(newBook.year)) {
      toast({
        title: "Error",
        description: "Year must be 4 digits",
        variant: "destructive"
      });
      return;
    }

    const result = await addBook(newBook.authorId, newBook.isbn.trim(), newBook.title.trim(), parseInt(newBook.year));
    
    if (result.success) {
      setNewBook({
        authorId: '',
        isbn: '',
        title: '',
        year: ''
      });
    }
  };

  const handleSearch = () => {
    // Search is handled automatically in useEffect
  };

  const handleDelete = async (id: string) => {
    await deleteBook(id);
  };

  const handleEdit = (book: Book) => {
    setEditingId(book.id);
    setEditForm({
      authorId: book.authorId,
      isbn: book.isbn,
      title: book.title,
      year: book.year.toString()
    });
    setIsEditModalOpen(true);
  };

  const handleSaveEdit = async () => {
    if (!editForm || !editingId) return;

    if (!editForm.authorId || !editForm.isbn?.trim() || !editForm.title?.trim() || !editForm.year?.trim()) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive"
      });
      return;
    }

    // Validate year
    const yearRegex = /^\d{4}$/;
    if (!yearRegex.test(editForm.year || '')) {
      toast({
        title: "Error",
        description: "Year must be 4 digits",
        variant: "destructive"
      });
      return;
    }

    const result = await updateBook(editingId, editForm.authorId, editForm.isbn, editForm.title, parseInt(editForm.year));
    
    if (result.success) {
      setEditingId(null);
      setEditForm({
        authorId: '',
        isbn: '',
        title: '',
        year: ''
      });
      setIsEditModalOpen(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditForm({
      authorId: '',
      isbn: '',
      title: '',
      year: ''
    });
    setIsEditModalOpen(false);
  };

  const handleSort = (field: 'title' | 'authorLastName' | 'isbn' | 'year') => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const sortedBooks = [...filteredBooks].sort((a, b) => {
    let aVal: string | number = '';
    let bVal: string | number = '';
    
    if (sortField === 'year') {
      aVal = a.year;
      bVal = b.year;
    } else {
      aVal = a[sortField]?.toString().toLowerCase() || '';
      bVal = b[sortField]?.toString().toLowerCase() || '';
    }
    
    if (sortDirection === 'asc') {
      return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    } else {
      return aVal > bVal ? -1 : aVal < bVal ? 1 : 0;
    }
  });

  const totalPages = Math.ceil(sortedBooks.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedBooks = sortedBooks.slice(startIndex, endIndex);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  if (booksLoading || authorsLoading) {
    return (
      <div className="container mx-auto max-w-7xl flex items-center justify-center py-8">
        <div className="text-lg text-card-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto max-w-7xl space-y-4 sm:space-y-6">
      {/* Add Book Form */}
      <div className="bg-card rounded-xl p-4 sm:p-6 shadow-lg border border-white/10">
        <h2 className="text-lg sm:text-xl font-semibold text-card-foreground mb-4">Add Book</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 items-end">
          <div className="sm:col-span-1">
            <label className="text-sm font-medium text-card-foreground block mb-2">Author</label>
            <Select value={newBook.authorId} onValueChange={(value) => setNewBook({...newBook, authorId: value})}>
              <SelectTrigger className="bg-input-bg border-0 text-input-foreground min-h-[44px]">
                <SelectValue placeholder="Select an author" />
              </SelectTrigger>
              <SelectContent>
                {authors.map((author) => (
                  <SelectItem key={author.id} value={author.id}>
                    {author.firstName} {author.lastName}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="sm:col-span-1">
            <label className="text-sm font-medium text-card-foreground block mb-2">ISBN</label>
            <Input
              value={newBook.isbn}
              onChange={(e) => setNewBook({...newBook, isbn: e.target.value})}
              placeholder="ISBN"
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
          <div className="sm:col-span-1">
            <label className="text-sm font-medium text-card-foreground block mb-2">Title</label>
            <Input
              value={newBook.title}
              onChange={(e) => setNewBook({...newBook, title: e.target.value})}
              placeholder="Title"
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
          <div className="sm:col-span-1">
            <label className="text-sm font-medium text-card-foreground block mb-2">Year</label>
            <Input
              value={newBook.year}
              onChange={(e) => setNewBook({...newBook, year: e.target.value})}
              placeholder="Year"
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
          <div className="col-span-full sm:col-span-1">
            <Button variant="action" onClick={handleAddBook} className="w-full min-h-[44px]">
              ADD
            </Button>
          </div>
        </div>
      </div>

      {/* Search Form */}
      <div className="bg-card rounded-xl p-4 sm:p-6 shadow-lg border border-white/10">
        <div className="flex flex-col sm:flex-row gap-4 items-end">
          <div className="flex-1 space-y-2">
            <label className="text-sm font-medium text-card-foreground">Search book</label>
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by name, first name, ISBN, title or year..."
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
        </div>
      </div>

      {/* Books Display - Table on desktop, Cards on mobile */}
      <div className="bg-card rounded-xl shadow-lg border border-white/10 overflow-hidden">
        {/* Desktop Table View */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-input-bg">
                <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[120px]">
                  <button 
                    onClick={() => handleSort('authorLastName')}
                    className="flex items-center gap-1 hover:text-primary transition-colors"
                  >
                    Last Name 
                    {sortField === 'authorLastName' && (
                      sortDirection === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[120px]">
                  First Name
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[150px]">
                  <button 
                    onClick={() => handleSort('isbn')}
                    className="flex items-center gap-1 hover:text-primary transition-colors"
                  >
                    ISBN 
                    {sortField === 'isbn' && (
                      sortDirection === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[200px]">
                  <button 
                    onClick={() => handleSort('title')}
                    className="flex items-center gap-1 hover:text-primary transition-colors"
                  >
                    Title
                    {sortField === 'title' && (
                      sortDirection === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[100px]">
                  <button 
                    onClick={() => handleSort('year')}
                    className="flex items-center gap-1 hover:text-primary transition-colors"
                  >
                    Year
                    {sortField === 'year' && (
                      sortDirection === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                </th>
                <th className="px-6 py-4 text-center text-sm font-semibold text-input-foreground min-w-[120px]">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {paginatedBooks.length > 0 ? (
                paginatedBooks.map((book, index) => (
                  <tr key={book.id} className={index % 2 === 0 ? 'bg-card' : 'bg-input-bg/20'}>
                    <td className="px-6 py-4">
                      <span className="text-card-foreground font-medium">{book.authorLastName}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-card-foreground">{book.authorFirstName}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-card-foreground font-mono text-sm">{book.isbn}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-card-foreground max-w-[200px] truncate block" title={book.title}>{book.title}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-card-foreground">{book.year}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center gap-2">
                        <Dialog open={isEditModalOpen && editingId === book.id} onOpenChange={setIsEditModalOpen}>
                          <DialogTrigger asChild>
                            <Button variant="icon" size="icon" onClick={() => handleEdit(book)} className="h-8 w-8">
                              <Edit className="h-4 w-4" />
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="sm:max-w-md mx-4">
                            <DialogHeader>
                              <DialogTitle>Edit Book</DialogTitle>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div className="space-y-2">
                                 <label className="text-sm font-medium">Author</label>
                                <Select value={editForm.authorId} onValueChange={(value) => setEditForm({...editForm, authorId: value})}>
                                  <SelectTrigger className="min-h-[44px]">
                                     <SelectValue placeholder="Select an author" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    {authors.map((author) => (
                                      <SelectItem key={author.id} value={author.id}>
                                        {author.firstName} {author.lastName}
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                              </div>
                              <div className="space-y-2">
                                <label className="text-sm font-medium">ISBN</label>
                                <Input
                                  value={editForm.isbn || ''}
                                  onChange={(e) => setEditForm({...editForm, isbn: e.target.value})}
                                  placeholder="ISBN"
                                  className="min-h-[44px]"
                                />
                              </div>
                              <div className="space-y-2">
                                 <label className="text-sm font-medium">Title</label>
                                <Input
                                  value={editForm.title || ''}
                                  onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                                   placeholder="Title"
                                  className="min-h-[44px]"
                                />
                              </div>
                              <div className="space-y-2">
                                 <label className="text-sm font-medium">Year</label>
                                <Input
                                  value={editForm.year || ''}
                                  onChange={(e) => setEditForm({...editForm, year: e.target.value})}
                                   placeholder="Year"
                                  className="min-h-[44px]"
                                />
                              </div>
                              <div className="flex flex-col sm:flex-row justify-end gap-2">
                                 <Button variant="outline" onClick={handleCancelEdit} className="w-full sm:w-auto min-h-[44px]">
                                   Cancel
                                 </Button>
                                 <Button variant="action" onClick={handleSaveEdit} className="w-full sm:w-auto min-h-[44px]">
                                   Save
                                 </Button>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                        <Button variant="destructive" size="icon" onClick={() => handleDelete(book.id)} className="h-8 w-8">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-card-foreground/60">
                    {searchQuery ? 'No results found' : 'No books available'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Mobile Card View */}
        <div className="md:hidden space-y-4 p-4">
          {paginatedBooks.length > 0 ? (
            paginatedBooks.map((book) => (
              <div key={book.id} className="bg-input-bg/20 rounded-lg p-4 space-y-3">
                <div className="flex justify-between items-start">
                  <div className="space-y-2 flex-1">
                    <h3 className="text-lg font-semibold text-card-foreground">{book.title}</h3>
                    <p className="text-card-foreground/80">
                      <span className="font-medium">{book.authorFirstName} {book.authorLastName}</span>
                    </p>
                    <div className="space-y-1">
                      <p className="text-sm text-card-foreground/70">
                        <span className="font-medium">ISBN:</span> {book.isbn}
                      </p>
                       <p className="text-sm text-card-foreground/70">
                         <span className="font-medium">Year:</span> {book.year}
                       </p>
                    </div>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <Dialog open={isEditModalOpen && editingId === book.id} onOpenChange={setIsEditModalOpen}>
                      <DialogTrigger asChild>
                        <Button variant="icon" size="icon" onClick={() => handleEdit(book)} className="h-10 w-10 min-h-[44px]">
                          <Edit className="h-5 w-5" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="mx-4 max-w-sm">
                         <DialogHeader>
                           <DialogTitle>Edit Book</DialogTitle>
                         </DialogHeader>
                        <div className="space-y-4">
                          <div className="space-y-2">
                            <label className="text-sm font-medium">Author</label>
                            <Select value={editForm.authorId} onValueChange={(value) => setEditForm({...editForm, authorId: value})}>
                              <SelectTrigger className="min-h-[44px]">
                                <SelectValue placeholder="Select an author" />
                              </SelectTrigger>
                              <SelectContent>
                                {authors.map((author) => (
                                  <SelectItem key={author.id} value={author.id}>
                                    {author.firstName} {author.lastName}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </div>
                          <div className="space-y-2">
                            <label className="text-sm font-medium">ISBN</label>
                            <Input
                              value={editForm.isbn || ''}
                              onChange={(e) => setEditForm({...editForm, isbn: e.target.value})}
                              placeholder="ISBN"
                              className="min-h-[44px]"
                            />
                          </div>
                          <div className="space-y-2">
                            <label className="text-sm font-medium">Title</label>
                            <Input
                              value={editForm.title || ''}
                              onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                              placeholder="Title"
                              className="min-h-[44px]"
                            />
                          </div>
                          <div className="space-y-2">
                            <label className="text-sm font-medium">Year</label>
                            <Input
                              value={editForm.year || ''}
                              onChange={(e) => setEditForm({...editForm, year: e.target.value})}
                              placeholder="Year"
                              className="min-h-[44px]"
                            />
                          </div>
                          <div className="flex flex-col gap-2">
                             <Button variant="action" onClick={handleSaveEdit} className="w-full min-h-[44px]">
                               Save
                             </Button>
                             <Button variant="outline" onClick={handleCancelEdit} className="w-full min-h-[44px]">
                               Cancel
                             </Button>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                    <Button variant="destructive" size="icon" onClick={() => handleDelete(book.id)} className="h-10 w-10 min-h-[44px]">
                      <Trash2 className="h-5 w-5" />
                    </Button>
                  </div>
                </div>
              </div>
            ))
          ) : (
             <div className="text-center py-8 text-card-foreground/60">
               {searchQuery ? 'No results found' : 'No books available'}
             </div>
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex flex-col sm:flex-row justify-center items-center gap-2 mt-4 p-4 border-t border-border">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="w-full sm:w-auto"
            >
              Previous
            </Button>
            
            <div className="flex gap-1 flex-wrap justify-center">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <Button
                  key={page}
                  variant={currentPage === page ? "action" : "outline"}
                  size="sm"
                  onClick={() => handlePageChange(page)}
                  className="w-8 h-8 text-xs"
                >
                  {page}
                </Button>
              ))}
            </div>
            
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="w-full sm:w-auto"
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};