default rel

extern fopen
extern fgets
extern fclose
extern strtol
extern printf

%define MAX_NUMBERS 10000
%define LINE_SIZE   65536

section .data
    mode_r      db "r", 0
    fmt_out     db "%s: %ld", 10, 0
    fmt_err     db "%s: файл испорчен", 10, 0
    no_name     db "(без имени)", 0

section .bss
    lineX       resb LINE_SIZE
    lineY       resb LINE_SIZE
    arrX        resq MAX_NUMBERS
    arrY        resq MAX_NUMBERS

section .text
    global main

; --- main ---
main:
    push    rbx
    push    r12
    push    r13
    push    r14
    push    r15

    ; --- default name ---
    lea     rbx, [no_name]
    cmp     edi, 2
    jl      .corrupted              
    mov     rbx, [rsi + 8]          

    ; --- open ---
    mov     rdi, rbx
    lea     rsi, [mode_r]
    call    fopen wrt ..plt
    test    rax, rax
    jz      .corrupted              
    mov     r12, rax                

    ; --- gets lineX ---
    lea     rdi, [lineX]
    mov     rsi, LINE_SIZE
    mov     rdx, r12
    call    fgets wrt ..plt
    test    rax, rax
    jz      .corrupted_close

    ; --- gets lineY ---
    lea     rdi, [lineY]
    mov     rsi, LINE_SIZE
    mov     rdx, r12
    call    fgets wrt ..plt
    test    rax, rax
    jz      .corrupted_close

    ; --- close file ---
    mov     rdi, r12
    call    fclose wrt ..plt

    ; --- Parse first line ---
    lea     rdi, [lineX]
    lea     rsi, [arrX]
    call    parse_line
    test    rax, rax
    jz      .corrupted              
    mov     r13, rax                

    ; --- Parse first line ---
    lea     rdi, [lineY]
    lea     rsi, [arrY]
    call    parse_line
    test    rax, rax
    jz      .corrupted
    mov     r14, rax                ;

    ; --- Check equals lenghts ---
    cmp     r13, r14
    jne     .corrupted

    ; --- Sum ---
    xor     rcx, rcx                
    xor     rdx, rdx                
    lea     r8, [arrX]
    lea     r9, [arrY]
.sum_loop:
    cmp     rcx, r13
    jge     .sum_done
    mov     rax, [r8 + rcx*8]
    sub     rax, [r9 + rcx*8]
    add     rdx, rax
    inc     rcx
    jmp     .sum_loop

.sum_done:
    ; --- Avg ---
    mov     rax, rdx
    cqo
    idiv    r13

    ; --- print ---
    lea     rdi, [fmt_out]
    mov     rsi, rbx
    mov     rdx, rax
    xor     eax, eax
    call    printf wrt ..plt

    xor     eax, eax
    jmp     .epilogue

; --- Error ---
.corrupted_close:
    mov     rdi, r12
    call    fclose wrt ..plt
.corrupted:
    lea     rdi, [fmt_err]
    mov     rsi, rbx
    xor     eax, eax
    call    printf wrt ..plt
    mov     eax, 1

.epilogue:
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    ret


parse_line:
    push    rbx
    push    r12
    push    r13
    push    r14
    push    r15
    sub     rsp, 16                 

    mov     r12, rdi               
    mov     r13, rsi                
    xor     r14, r14               

.next_number:
    ; --- Skip separator ---
.skip:
    movzx   eax, byte [r12]
    test    al, al
    jz      .done
    cmp     al, ' '
    je      .skip_inc
    cmp     al, 9
    je      .skip_inc
    cmp     al, 10
    je      .skip_inc
    cmp     al, 13
    je      .skip_inc
    cmp     al, ','
    je      .skip_inc
    jmp     .parse

.skip_inc:
    inc     r12
    jmp     .skip

.parse:
    mov     rdi, r12
    lea     rsi, [rsp]
    mov     edx, 10
    call    strtol wrt ..plt

    mov     rbx, [rsp]
    cmp     rbx, r12
    je      .error

    movzx   ecx, byte [rbx]
    test    cl, cl
    jz      .store
    cmp     cl, ' '
    je      .store
    cmp     cl, 9
    je      .store
    cmp     cl, 10
    je      .store
    cmp     cl, 13
    je      .store
    cmp     cl, ','
    je      .store
    jmp     .error

.store:
    cmp     r14, MAX_NUMBERS
    jge     .error
    mov     [r13 + r14*8], rax
    inc     r14
    mov     r12, rbx
    jmp     .next_number

.done:
    mov     rax, r14
    jmp     .return

.error:
    xor     eax, eax

.return:
    add     rsp, 16
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    ret