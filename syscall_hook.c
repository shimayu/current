#include <linux/kernel.h>
#include <linux/module.h>
#include <asm/unistd.h>
#include <linux/string.h>
#include <kernel/kallsyms.c>

MODULE_AUTHOR("shimady");
MODULE_LICENSE("GPL");

extern void* sys_call_table[];

asmlinkage static int (*original_open)(const char* pathname, int flags, umode_t mode);

asmlinkage static int my_open(const char* pathname, int flags, umode_t mode)
{
	printk(KERN_INFO "my_open(\"%s\", %d, %u)\n", pathname, flags, mode);
	if (strcmp(pathname, "/bin/sleep") == 0) {
		return ENOENT;
	} else {
		return original_open(pathname, flags, mode);
	}
}

static int __init my_open_init(void)
{
	printk(KERN_INFO "my_open: init\n");
	/* sys_call_table = kallsyms_lookup_name("sys_call_table"); */
	original_open = sys_call_table[__NR_open];
	sys_call_table[__NR_open] = my_open;
	
	return 0;
}

module_init(my_open_init);

static void __exit my_open_exit(void)
{
	printk(KERN_INFO "my_open: exit\n");
	sys_call_table[__NR_open] = original_open;
}

module_exit(my_open_exit);

