# Pylisper - a simple LISP interpreter

Pylisper is a simple lisp interpreter. Simple in implementation and simple in implemented dialect.
In spirit of simplicity pylisper implements repl only (however you are free to extend it to reading files).

## Running from source

Pylisper is build using `poetry` [https://python-poetry.org/].
Simply `cd` into the project directory and run:
```
$ poetry install
$ poetry run repl
```
to start an interactive console.

## What can it do?

Pylisper understands everything original lisp did but a bit differently and adds some more.

Symbols and natural numbers are supported as atoms.
Lists are supported as expected.

Quoting can only be done with a `quote` special form.
Line comments start with `;;` and, as line comments do, last to the end of the line.

True and False literals are available as `#t` and `#f` respectively.

## Special forms

### define

```
(define $symbol $value)
```

Can used to create local and global variables. You can use it to redefine variables as well.
Returns an empty list.
When used inside a function creates a local variable.
When used at top level creates a global variable.


```
(define global 10) ;; defines a global variable named "global"
(define func
    (lambda (x) (begin ;; assigning a lambda creates a named function
        (define local 10) ;; creates a local variable named "local"
        (+ local x))))
```

Using define to assign a name to a function also allows for recursive calls.

```
(define rec
    (lambda (x) (cond
        ((= x 0) (quote end))
        (#t (rec (- x 1))))))
```

### set!
```
(set! $memory $val)
```
Set special form sets the value under the pointed memory to the passed value.
Returns an empty list
A memory reference can be a symbol or a cell (which can be obtained by using `car` on a list).

```
(define global (quote ()))
(define list (quote (0 0 0)))
(define func
    (lambda (x)
        (set! global x)))
(define range
    (lambda (l num) (cond
        ((null? (cdr l)) (set! (car l) num))
        (#t (begin
            (set! (car l) num)
            (range (cdr l) (+ num 1)))))))
```

### quote
```
(quote $expr)
```

Simply returns expression without evaluating it.
Can be used to make operations on symbols or creating lists.

```
(quote (1 2 3 4)) ;; creates a list (1 2 3 4)
(quote Hello) ;; returns symbol without evaluating it
(quote ()) ;; creates an empty list
```

### cond
```
(cond $arms)
```
Can have one or more arms. Each arm is a form `($pred $expr)`

Condition form checks predicate in each arm in sequence and if true evaluates and returns expression associated with a predicate. If every predicate evaluated to `False` then empty list is returned.

True symbol (`#t`) can be used to create a catch-all arm.

```
(lambda (x)
    (cond
        ((= x 0) (quote zero))
        ((= x 1) (quote one))
        (#t (quote smth-else))))

;; if-then-else like condition
(cond
    (pred (quote then))
    (#t (quote else)))
```

### begin
```
(begin $exprs)
```

Executes expressions in sequence and returns value of the last one.
Can be used to perform side effects.

```
(begin
    (set! mem 10) ;; set val of mem variable to 10
    (use-mem)) ;; call function that uses mem internally
```

### lambda
```
(lambda $args $body)
```

Creates a lexically scoped lambda function.
Lambda arguments should be a list of symbols.
If lambda should take no arguments then empty list should be passed.
Body can be any expression that will be evaluated when lambda is called.
Lambdas can be called as is, without a need to bound them to a name.
```
;; lambda that takes no arguments bound to name `ret-hello`
(define ret-hello (lambda () (quote hello)))

;; curried add function
(define add (lambda (x) (lambda (y) (+ x y))))

;; lambda called as is
((lambda (x y) (+ x y)) 10 15) ;; returns 25
```

## Standard functions

Some functions are already there for your convenience.

- `cons`, creates a cell from a value and appends it to the front of a list;
- `car`, gets head of a list;
- `cdr`, gets tail of a list;
- `eq?`, checks if two values are kept under the same memory (true for the same symbols);
- `null?`, checks if the list is empty;
- `atom?`, checks if the passed value is a symbol or a number;
- `not`, negates boolean value;
- `=`, checks if two values are equal;
- `+`, adds two values;
- `-`, subtracts two values;

## Limitations

There are no tail call optimizations and because of the way
interpreter is implemented recursion stack is pretty shallow as
it reuses pythons stack.

Macros were not something that was planned to be implemented so
there are not any.

And there are probably some errors in the standard library functions
as most of them are there just for development purposes.
