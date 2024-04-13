import { useToast } from "./components/ui/toast"

const { toast } = useToast()

export const notifyError = (errorType: string, message: string) => {
    toast({
        title: errorType,
        description: message,
        variant: "destructive"
    })
}

export const notifySuccess = (message: string) => {
    toast({
        title: "Completed",
        description: message,
    })
}