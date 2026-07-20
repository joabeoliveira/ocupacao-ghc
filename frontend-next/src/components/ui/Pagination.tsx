import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './Button';

interface PaginationProps {
  currentPage: number;
  totalItems: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ currentPage, totalItems, pageSize, onPageChange }: PaginationProps) {
  const totalPages = Math.ceil(totalItems / pageSize) || 1;

  return (
    <div className="flex items-center justify-between mt-4 bg-white px-4 py-3 rounded-lg border border-panel-border sm:px-6 shadow-sm">
      <div className="flex flex-1 justify-between sm:hidden">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(Math.max(currentPage - 1, 1))}
          disabled={currentPage === 1}
        >
          Anterior
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(Math.min(currentPage + 1, totalPages))}
          disabled={currentPage === totalPages}
        >
          Próximo
        </Button>
      </div>
      <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p className="text-xs text-muted">
            Mostrando <span className="font-semibold text-text">{Math.min((currentPage - 1) * pageSize + 1, totalItems)}</span>{' '}
            até{' '}
            <span className="font-semibold text-text">
              {Math.min(currentPage * pageSize, totalItems)}
            </span>{' '}
            de <span className="font-semibold text-text">{totalItems}</span> registros
          </p>
        </div>
        <div>
          <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
            <button
              onClick={() => onPageChange(Math.max(currentPage - 1, 1))}
              disabled={currentPage === 1}
              className="relative inline-flex items-center rounded-l-md px-2.5 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <span className="sr-only">Anterior</span>
              <ChevronLeft className="h-4 w-4" aria-hidden="true" />
            </button>
            
            {Array.from({ length: Math.min(5, totalPages) }).map((_, index) => {
              // Basic page indicator around the current page
              let pageNumber = index + 1;
              if (currentPage > 3 && totalPages > 5) {
                pageNumber = currentPage - 3 + index;
                if (pageNumber + (4 - index) > totalPages) {
                  pageNumber = totalPages - 4 + index;
                }
              }

              return (
                <button
                  key={pageNumber}
                  onClick={() => onPageChange(pageNumber)}
                  className={`relative inline-flex items-center px-4 py-2 text-xs font-semibold ring-1 ring-inset focus:z-20 focus:outline-offset-0 ${
                    currentPage === pageNumber
                      ? 'z-10 bg-ghc-blue text-white ring-ghc-blue'
                      : 'text-gray-900 ring-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {pageNumber}
                </button>
              );
            })}

            <button
              onClick={() => onPageChange(Math.min(currentPage + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="relative inline-flex items-center rounded-r-md px-2.5 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <span className="sr-only">Próximo</span>
              <ChevronRight className="h-4 w-4" aria-hidden="true" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  );
}
