import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import { 
  Home, 
  FileText, 
  Calendar, 
  DollarSign, 
  AlertTriangle,
  CheckCircle,
  Clock,
  TrendingUp,
  Users,
  Building,
  Phone,
  Mail,
  MapPin,
  Download,
  Upload,
  Eye,
  Edit,
  MoreHorizontal
} from 'lucide-react'
import './App.css'

// Mock transaction data
const mockTransactions = [
  {
    id: 1,
    property: {
      address: "123 Main Street",
      city: "Anytown",
      state: "CA",
      zipCode: "12345",
      price: 450000,
      type: "Single Family"
    },
    client: {
      name: "John Smith",
      email: "john.smith@email.com",
      phone: "(555) 123-4567",
      type: "Buyer"
    },
    status: "Under Contract",
    contractDate: "2024-08-01",
    closingDate: "2024-08-28",
    progress: 65,
    riskScore: 25,
    riskLevel: "Low",
    listingAgent: "Sarah Johnson",
    buyerAgent: "Mike Rodriguez",
    commission: 13500,
    milestones: [
      { name: "Contract Signed", completed: true, date: "2024-08-01", status: "Complete" },
      { name: "Inspection Scheduled", completed: true, date: "2024-08-05", status: "Complete" },
      { name: "Inspection Complete", completed: true, date: "2024-08-07", status: "Complete" },
      { name: "Appraisal Ordered", completed: true, date: "2024-08-10", status: "Complete" },
      { name: "Appraisal Complete", completed: false, date: "2024-08-15", status: "In Progress" },
      { name: "Final Walkthrough", completed: false, date: "2024-08-26", status: "Pending" },
      { name: "Closing", completed: false, date: "2024-08-28", status: "Pending" }
    ],
    documents: [
      { name: "Purchase Agreement", status: "Signed", date: "2024-08-01", type: "Contract" },
      { name: "Inspection Report", status: "Complete", date: "2024-08-07", type: "Report" },
      { name: "Appraisal Report", status: "Pending", date: "2024-08-15", type: "Report" },
      { name: "Loan Documents", status: "In Review", date: "2024-08-12", type: "Financial" }
    ]
  },
  {
    id: 2,
    property: {
      address: "456 Oak Avenue",
      city: "Anytown", 
      state: "CA",
      zipCode: "12346",
      price: 325000,
      type: "Condo"
    },
    client: {
      name: "Sarah Wilson",
      email: "sarah.w@email.com",
      phone: "(555) 234-5678",
      type: "Seller"
    },
    status: "Inspection Period",
    contractDate: "2024-08-08",
    closingDate: "2024-09-05",
    progress: 35,
    riskScore: 45,
    riskLevel: "Medium",
    listingAgent: "Jennifer Lee",
    buyerAgent: "Robert Taylor",
    commission: 9750,
    milestones: [
      { name: "Contract Signed", completed: true, date: "2024-08-08", status: "Complete" },
      { name: "Inspection Scheduled", completed: true, date: "2024-08-12", status: "Complete" },
      { name: "Inspection Complete", completed: false, date: "2024-08-14", status: "In Progress" },
      { name: "Appraisal Ordered", completed: false, date: "2024-08-17", status: "Pending" },
      { name: "Appraisal Complete", completed: false, date: "2024-08-24", status: "Pending" },
      { name: "Final Walkthrough", completed: false, date: "2024-09-03", status: "Pending" },
      { name: "Closing", completed: false, date: "2024-09-05", status: "Pending" }
    ],
    documents: [
      { name: "Purchase Agreement", status: "Signed", date: "2024-08-08", type: "Contract" },
      { name: "Seller Disclosures", status: "Complete", date: "2024-08-09", type: "Disclosure" },
      { name: "Inspection Report", status: "Pending", date: "2024-08-14", type: "Report" }
    ]
  },
  {
    id: 3,
    property: {
      address: "789 Pine Road",
      city: "Anytown",
      state: "CA", 
      zipCode: "12347",
      price: 650000,
      type: "Single Family"
    },
    client: {
      name: "Mike Davis",
      email: "mike.d@email.com",
      phone: "(555) 345-6789",
      type: "Buyer"
    },
    status: "Clear to Close",
    contractDate: "2024-07-20",
    closingDate: "2024-08-25",
    progress: 90,
    riskScore: 15,
    riskLevel: "Low",
    listingAgent: "Sarah Johnson",
    buyerAgent: "Michael Rodriguez",
    commission: 19500,
    milestones: [
      { name: "Contract Signed", completed: true, date: "2024-07-20", status: "Complete" },
      { name: "Inspection Scheduled", completed: true, date: "2024-07-25", status: "Complete" },
      { name: "Inspection Complete", completed: true, date: "2024-07-27", status: "Complete" },
      { name: "Appraisal Ordered", completed: true, date: "2024-07-30", status: "Complete" },
      { name: "Appraisal Complete", completed: true, date: "2024-08-05", status: "Complete" },
      { name: "Final Walkthrough", completed: false, date: "2024-08-23", status: "Scheduled" },
      { name: "Closing", completed: false, date: "2024-08-25", status: "Scheduled" }
    ],
    documents: [
      { name: "Purchase Agreement", status: "Signed", date: "2024-07-20", type: "Contract" },
      { name: "Inspection Report", status: "Complete", date: "2024-07-27", type: "Report" },
      { name: "Appraisal Report", status: "Complete", date: "2024-08-05", type: "Report" },
      { name: "Loan Documents", status: "Approved", date: "2024-08-10", type: "Financial" },
      { name: "Title Report", status: "Clear", date: "2024-08-12", type: "Title" }
    ]
  }
]

const mockMetrics = {
  totalActive: 15,
  closingThisWeek: 3,
  atRisk: 2,
  totalVolume: 4250000,
  avgDaysToClose: 32,
  successRate: 94
}

function TransactionCard({ transaction, onClick }) {
  const getRiskColor = (level) => {
    switch(level) {
      case 'High': return 'bg-red-100 text-red-800'
      case 'Medium': return 'bg-yellow-100 text-yellow-800'
      case 'Low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status) => {
    switch(status) {
      case 'Clear to Close': return 'bg-green-100 text-green-800'
      case 'Under Contract': return 'bg-blue-100 text-blue-800'
      case 'Inspection Period': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => onClick(transaction)}>
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-lg">{transaction.property.address}</CardTitle>
            <CardDescription>{transaction.property.city}, {transaction.property.state}</CardDescription>
          </div>
          <Badge className={getRiskColor(transaction.riskLevel)}>
            {transaction.riskLevel} Risk
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Status</span>
            <Badge className={getStatusColor(transaction.status)}>
              {transaction.status}
            </Badge>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Progress</span>
            <span className="text-sm font-medium">{transaction.progress}%</span>
          </div>
          <Progress value={transaction.progress} className="w-full" />
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Closing Date</span>
            <span className="text-sm font-medium">{transaction.closingDate}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Sale Price</span>
            <span className="text-sm font-medium">${transaction.property.price.toLocaleString()}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Client</span>
            <span className="text-sm font-medium">{transaction.client.name}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function TransactionDetail({ transaction, onBack }) {
  if (!transaction) return null

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="outline" onClick={onBack}>
          ← Back to Dashboard
        </Button>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Edit className="h-4 w-4 mr-2" />
            Edit
          </Button>
          <Button variant="outline" size="sm">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Property Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Building className="h-5 w-5 mr-2" />
              Property Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <p className="font-medium">{transaction.property.address}</p>
              <p className="text-sm text-gray-600">
                {transaction.property.city}, {transaction.property.state} {transaction.property.zipCode}
              </p>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Type</span>
              <span className="text-sm font-medium">{transaction.property.type}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Sale Price</span>
              <span className="text-sm font-medium">${transaction.property.price.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Commission</span>
              <span className="text-sm font-medium">${transaction.commission.toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>

        {/* Client Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="h-5 w-5 mr-2" />
              Client Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <p className="font-medium">{transaction.client.name}</p>
              <p className="text-sm text-gray-600">{transaction.client.type}</p>
            </div>
            <div className="flex items-center space-x-2">
              <Mail className="h-4 w-4 text-gray-400" />
              <span className="text-sm">{transaction.client.email}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Phone className="h-4 w-4 text-gray-400" />
              <span className="text-sm">{transaction.client.phone}</span>
            </div>
            <div className="pt-2">
              <p className="text-sm text-gray-600">Listing Agent</p>
              <p className="font-medium">{transaction.listingAgent}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Buyer Agent</p>
              <p className="font-medium">{transaction.buyerAgent}</p>
            </div>
          </CardContent>
        </Card>

        {/* Transaction Status */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Transaction Status
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Status</span>
              <Badge>{transaction.status}</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Progress</span>
              <span className="font-medium">{transaction.progress}%</span>
            </div>
            <Progress value={transaction.progress} className="w-full" />
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Risk Level</span>
              <Badge variant={transaction.riskLevel === 'Low' ? 'default' : 'destructive'}>
                {transaction.riskLevel} Risk
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Contract Date</span>
              <span className="text-sm font-medium">{transaction.contractDate}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Closing Date</span>
              <span className="text-sm font-medium">{transaction.closingDate}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Milestones and Documents */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Milestones */}
        <Card>
          <CardHeader>
            <CardTitle>Transaction Milestones</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {transaction.milestones.map((milestone, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-1">
                    {milestone.completed ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : milestone.status === 'In Progress' ? (
                      <Clock className="h-5 w-5 text-blue-500" />
                    ) : (
                      <div className="h-5 w-5 rounded-full border-2 border-gray-300" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={`font-medium ${milestone.completed ? 'text-gray-900' : 'text-gray-500'}`}>
                      {milestone.name}
                    </p>
                    <p className="text-sm text-gray-600">{milestone.date}</p>
                    <Badge variant="outline" className="mt-1">
                      {milestone.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Documents */}
        <Card>
          <CardHeader>
            <CardTitle>Transaction Documents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {transaction.documents.map((doc, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <FileText className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="font-medium">{doc.name}</p>
                      <p className="text-sm text-gray-600">{doc.type} • {doc.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant={doc.status === 'Complete' || doc.status === 'Signed' ? 'default' : 'secondary'}>
                      {doc.status}
                    </Badge>
                    <Button variant="outline" size="sm">
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full">
                <Upload className="h-4 w-4 mr-2" />
                Upload Document
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function Dashboard() {
  const [selectedTransaction, setSelectedTransaction] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')

  if (selectedTransaction) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <TransactionDetail 
            transaction={selectedTransaction} 
            onBack={() => setSelectedTransaction(null)} 
          />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Home className="h-8 w-8 text-blue-600" />
              <h1 className="ml-2 text-xl font-semibold text-gray-900">Transaction Management</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Upload className="h-4 w-4 mr-2" />
                Import
              </Button>
              <Button size="sm">
                <FileText className="h-4 w-4 mr-2" />
                New Transaction
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="active">Active Deals</TabsTrigger>
            <TabsTrigger value="closing">Closing Soon</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Active Transactions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{mockMetrics.totalActive}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Closing This Week</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">{mockMetrics.closingThisWeek}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">At Risk</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">{mockMetrics.atRisk}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Total Volume</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${(mockMetrics.totalVolume / 1000000).toFixed(1)}M</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Avg Days to Close</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{mockMetrics.avgDaysToClose}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Success Rate</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">{mockMetrics.successRate}%</div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Transactions */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Transactions</CardTitle>
                <CardDescription>Latest transaction activity and status updates</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {mockTransactions.map((transaction) => (
                    <TransactionCard 
                      key={transaction.id} 
                      transaction={transaction}
                      onClick={setSelectedTransaction}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Active Deals Tab */}
          <TabsContent value="active" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {mockTransactions.filter(t => t.status !== 'Closed').map((transaction) => (
                <TransactionCard 
                  key={transaction.id} 
                  transaction={transaction}
                  onClick={setSelectedTransaction}
                />
              ))}
            </div>
          </TabsContent>

          {/* Closing Soon Tab */}
          <TabsContent value="closing" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {mockTransactions.filter(t => {
                const closingDate = new Date(t.closingDate)
                const today = new Date()
                const daysUntilClosing = Math.ceil((closingDate - today) / (1000 * 60 * 60 * 24))
                return daysUntilClosing <= 7 && daysUntilClosing >= 0
              }).map((transaction) => (
                <TransactionCard 
                  key={transaction.id} 
                  transaction={transaction}
                  onClick={setSelectedTransaction}
                />
              ))}
            </div>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Transaction Pipeline</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span>Under Contract</span>
                      <span className="font-medium">8 deals</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Inspection Period</span>
                      <span className="font-medium">3 deals</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Clear to Close</span>
                      <span className="font-medium">4 deals</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Risk Assessment</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="flex items-center">
                        <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                        Low Risk
                      </span>
                      <span className="font-medium">11 deals</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="flex items-center">
                        <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                        Medium Risk
                      </span>
                      <span className="font-medium">3 deals</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="flex items-center">
                        <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                        High Risk
                      </span>
                      <span className="font-medium">1 deal</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

function App() {
  return (
    <Router>
      <div className="App">
        <Dashboard />
      </div>
    </Router>
  )
}

export default App
