package main

import "fmt"

func closure01() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

func main() {
	myfun := closure01()
	for i := 0; i < 3; i++ {
		fmt.Println(myfun(i))
		//调用 myfun 会执行closure01()内部的匿名函数，i作为参数传递给该函数的变量x，sum就是“附有的数据”
	}
}
