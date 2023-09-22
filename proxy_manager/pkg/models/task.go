package models

type Task struct {
	Interval string
	Name     string
	Func     func()
}

func NewTask(interval, name string, fn func()) *Task {
	return &Task{
		Interval: interval,
		Name:     name,
		Func:     fn,
	}
}
