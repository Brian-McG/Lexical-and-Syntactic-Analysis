	.text
	.file	"<string>"
	.section	.rodata.cst4,"aM",@progbits,4
	.align	4
.LCPI0_0:
	.long	1106981684
	.text
	.globl	main
	.align	16, 0x90
	.type	main,@function
main:
	.cfi_startproc
	pushq	%rax
.Ltmp0:
	.cfi_def_cfa_offset 16
	movl	$1084227584, 4(%rsp)
	movl	$1106981684, (%rsp)
	movabsq	$.LCPI0_0, %rax
	movss	(%rax), %xmm0
	popq	%rax
	retq
.Ltmp1:
	.size	main, .Ltmp1-main
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits

