package main

import "fmt"

// START OMIT
func closure02(fn func(int, int) int) func(int) int {
	tmp := 1
	return func(x int) int {
		return fn(x, tmp)
	}
}

func add(x int, y int) int {
	return x + y
}

func sub(x int, y int) int {
	return x - y
}

// END OMIT

// START MAIN OMIT
func main() {
	// closure02 稍微复杂一点 —— 它的参数中有一函数类型的变量fn，在内部的匿名函数里调用了fn， 这里嵌套了一层
	myadd := closure02(add)
	fmt.Println(myadd(1))
	// 调用 myadd 会执行 closure02 内部的匿名函数，匿名函数又会执行作为参数传递的函数fn， 函数fn的参数x就是myadd(1)中的1，参数y就是附有数据tmp，所以最终结果就是 x(1) + y(tmp=1) = 2
	mysub := closure02(sub)
	fmt.Println(mysub(1))
	// 同上
}

// END MAIN OMIT
