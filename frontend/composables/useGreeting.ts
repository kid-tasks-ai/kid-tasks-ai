export const useGreeting = () => {
  const createGreeting = (name: string) => {
    return `Привет, ${name}!`
  }

  return {
    createGreeting
  }
}
