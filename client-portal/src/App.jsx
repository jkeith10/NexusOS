import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import { 
  Home, 
  FileText, 
  MessageSquare, 
  Calendar, 
  DollarSign, 
  User, 
  LogOut,
  Phone,
  Mail,
  MapPin,
  Clock,
  CheckCircle,
  AlertCircle,
  Download
} from 'lucide-react'
import './App.css'

// Mock data - in real implementation, this would come from API
const mockClient = {
  id: 1,
  firstName: "John",
  lastName: "Smith",
  email: "john.smith@email.com",
  phone: "(555) 123-4567",
  agent: {
    name: "Sarah Johnson",
    email: "sarah@realestate.com",
    phone: "(555) 987-6543",
    photo: "/api/placeholder/150/150"
  }
}

const mockTransaction = {
  id: 1,
  type: "Purchase",
  property: {
    address: "123 Main Street",
    city: "Anytown",
    state: "CA",
    zipCode: "12345",
    price: 450000,
    photos: ["/api/placeholder/400/300"]
  },
  status: "Under Contract",
  contractDate: "2024-01-15",
  closingDate: "2024-02-28",
  progress: 65,
  milestones: [
    { name: "Contract Signed", completed: true, date: "2024-01-15" },
    { name: "Inspection Scheduled", completed: true, date: "2024-01-20" },
    { name: "Inspection Complete", completed: true, date: "2024-01-25" },
    { name: "Appraisal Ordered", completed: true, date: "2024-01-28" },
    { name: "Appraisal Complete", completed: false, date: "2024-02-05" },
    { name: "Final Walkthrough", completed: false, date: "2024-02-26" },
    { name: "Closing", completed: false, date: "2024-02-28" }
  ]
}

const mockDocuments = [
  { id: 1, name: "Purchase Agreement", type: "Contract", date: "2024-01-15", status: "Signed" },
  { id: 2, name: "Inspection Report", type: "Report", date: "2024-01-25", status: "Complete" },
  { id: 3, name: "Appraisal Report", type: "Report", date: "2024-02-05", status: "Pending" },
  { id: 4, name: "Loan Documents", type: "Financial", date: "2024-02-10", status: "In Review" }
]

const mockMessages = [
  {
    id: 1,
    from: "Sarah Johnson",
    message: "Great news! The inspection went well. Only minor items found.",
    timestamp: "2024-01-25 14:30",
    type: "agent"
  },
  {
    id: 2,
    from: "You",
    message: "That's wonderful! When will we get the full report?",
    timestamp: "2024-01-25 15:45",
    type: "client"
  },
  {
    id: 3,
    from: "Sarah Johnson",
    message: "The full report should be available by end of day. I'll upload it to your portal.",
    timestamp: "2024-01-25 16:00",
    type: "agent"
  }
]

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    // Mock login - in real implementation, this would validate credentials
    if (email && password) {
      onLogin(mockClient)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Client Portal</CardTitle>
          <CardDescription>Sign in to access your real estate dashboard</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full">
              Sign In
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

function Dashboard({ client, onLogout }) {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Home className="h-8 w-8 text-blue-600" />
              <h1 className="ml-2 text-xl font-semibold text-gray-900">Real Estate Portal</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Welcome, {client.firstName}</span>
              <Button variant="outline" size="sm" onClick={onLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="transaction">Transaction</TabsTrigger>
            <TabsTrigger value="documents">Documents</TabsTrigger>
            <TabsTrigger value="messages">Messages</TabsTrigger>
            <TabsTrigger value="profile">Profile</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Transaction Status */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <DollarSign className="h-5 w-5 mr-2" />
                    Transaction Status
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Progress</span>
                      <span className="text-sm font-medium">{mockTransaction.progress}%</span>
                    </div>
                    <Progress value={mockTransaction.progress} className="w-full" />
                    <Badge variant="secondary">{mockTransaction.status}</Badge>
                  </div>
                </CardContent>
              </Card>

              {/* Property Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <MapPin className="h-5 w-5 mr-2" />
                    Property
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="font-medium">{mockTransaction.property.address}</p>
                    <p className="text-sm text-gray-600">
                      {mockTransaction.property.city}, {mockTransaction.property.state} {mockTransaction.property.zipCode}
                    </p>
                    <p className="text-lg font-bold text-green-600">
                      ${mockTransaction.property.price.toLocaleString()}
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Agent Contact */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <User className="h-5 w-5 mr-2" />
                    Your Agent
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src={client.agent.photo} />
                      <AvatarFallback>{client.agent.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium">{client.agent.name}</p>
                      <p className="text-sm text-gray-600">{client.agent.phone}</p>
                    </div>
                  </div>
                  <div className="mt-4 space-y-2">
                    <Button variant="outline" size="sm" className="w-full">
                      <Phone className="h-4 w-4 mr-2" />
                      Call Agent
                    </Button>
                    <Button variant="outline" size="sm" className="w-full">
                      <Mail className="h-4 w-4 mr-2" />
                      Send Message
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockTransaction.milestones.slice(0, 3).map((milestone, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      {milestone.completed ? (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      ) : (
                        <Clock className="h-5 w-5 text-gray-400" />
                      )}
                      <div className="flex-1">
                        <p className="font-medium">{milestone.name}</p>
                        <p className="text-sm text-gray-600">{milestone.date}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Transaction Tab */}
          <TabsContent value="transaction" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Transaction Timeline</CardTitle>
                <CardDescription>Track your real estate transaction progress</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {mockTransaction.milestones.map((milestone, index) => (
                    <div key={index} className="flex items-start space-x-4">
                      <div className="flex-shrink-0">
                        {milestone.completed ? (
                          <CheckCircle className="h-6 w-6 text-green-500" />
                        ) : (
                          <div className="h-6 w-6 rounded-full border-2 border-gray-300" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`font-medium ${milestone.completed ? 'text-gray-900' : 'text-gray-500'}`}>
                          {milestone.name}
                        </p>
                        <p className="text-sm text-gray-600">{milestone.date}</p>
                      </div>
                      <div className="flex-shrink-0">
                        {milestone.completed && (
                          <Badge variant="secondary">Complete</Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Documents Tab */}
          <TabsContent value="documents" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Transaction Documents</CardTitle>
                <CardDescription>Access and download your transaction documents</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockDocuments.map((doc) => (
                    <div key={doc.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-gray-400" />
                        <div>
                          <p className="font-medium">{doc.name}</p>
                          <p className="text-sm text-gray-600">{doc.type} • {doc.date}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Badge variant={doc.status === 'Signed' ? 'default' : 'secondary'}>
                          {doc.status}
                        </Badge>
                        <Button variant="outline" size="sm">
                          <Download className="h-4 w-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Messages Tab */}
          <TabsContent value="messages" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Messages</CardTitle>
                <CardDescription>Communicate with your agent</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {mockMessages.map((message) => (
                    <div key={message.id} className={`flex ${message.type === 'client' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.type === 'client' 
                          ? 'bg-blue-500 text-white' 
                          : 'bg-gray-100 text-gray-900'
                      }`}>
                        <p className="text-sm">{message.message}</p>
                        <p className={`text-xs mt-1 ${
                          message.type === 'client' ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          {message.timestamp}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-4 flex space-x-2">
                  <Input placeholder="Type your message..." className="flex-1" />
                  <Button>Send</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Profile Tab */}
          <TabsContent value="profile" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Profile Information</CardTitle>
                <CardDescription>Your contact information and preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="firstName">First Name</Label>
                    <Input id="firstName" value={client.firstName} readOnly />
                  </div>
                  <div>
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input id="lastName" value={client.lastName} readOnly />
                  </div>
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" value={client.email} readOnly />
                  </div>
                  <div>
                    <Label htmlFor="phone">Phone</Label>
                    <Input id="phone" value={client.phone} readOnly />
                  </div>
                </div>
                <Button variant="outline">Edit Profile</Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

function App() {
  const [client, setClient] = useState(null)

  const handleLogin = (clientData) => {
    setClient(clientData)
  }

  const handleLogout = () => {
    setClient(null)
  }

  return (
    <Router>
      <div className="App">
        {client ? (
          <Dashboard client={client} onLogout={handleLogout} />
        ) : (
          <LoginForm onLogin={handleLogin} />
        )}
      </div>
    </Router>
  )
}

export default App

