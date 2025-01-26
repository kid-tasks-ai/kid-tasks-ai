export default defineNuxtPlugin(() => {
    const toast = useToast()

    return {
        provide: {
            notify: {
                success(message: string) {
                    toast.add({
                        title: 'Успешно',
                        description: message,
                        color: 'green'
                    })
                },
                error(message: string) {
                    toast.add({
                        title: 'Ошибка',
                        description: message,
                        color: 'red'
                    })
                },
                info(message: string) {
                    toast.add({
                        title: 'Информация',
                        description: message,
                        color: 'blue'
                    })
                }
            }
        }
    }
})