import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Leaf, Car, Lightbulb, ShoppingCart, Users, Award, Map, Trash, Recycle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const generateRandomData = () => {
  const carbonFootprint = [
    { name: 'Transport', value: Math.floor(Math.random() * 50) + 10 },
    { name: 'Energy', value: Math.floor(Math.random() * 50) + 10 },
    { name: 'Consumption', value: Math.floor(Math.random() * 50) + 10 },
    { name: 'Waste', value: Math.floor(Math.random() * 30) + 5 },
  ];

  const dailyActivities = [...Array(7)].map((_, i) => ({
    name: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i],
    points: Math.floor(Math.random() * 200) + 50,
  }));

  const monthlyProgress = [...Array(12)].map((_, i) => ({
    name: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i],
    carbonReduction: Math.floor(Math.random() * 100),
  }));

  return {
    carbonFootprint,
    ecoPoints: Math.floor(Math.random() * 5000) + 500,
    communityRank: Math.floor(Math.random() * 100) + 1,
    dailyActivities,
    monthlyProgress,
  };
};

const EcoCitizenshipPlatform = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [data, setData] = useState(generateRandomData());
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setData(generateRandomData());
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const addNotification = (message) => {
    setNotifications(prev => [...prev, message]);
    setTimeout(() => setNotifications(prev => prev.slice(1)), 3000);
  };

  const logActivity = (activity) => {
    setData(prev => ({
      ...prev,
      ecoPoints: prev.ecoPoints + Math.floor(Math.random() * 50) + 10,
    }));
    addNotification(Logged ${activity}! Eco points updated.);
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-green-600 text-white p-4 shadow-md">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold">EcoCitizen</h1>
          <div className="flex items-center space-x-4">
            <div className="bg-green-500 rounded-full p-2">
              <Leaf size={24} />
            </div>
            <span className="text-xl font-semibold">{data.ecoPoints} Points</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {notifications.map((notification, index) => (
          <Alert key={index} className="mb-4">
            <AlertTitle>Update</AlertTitle>
            <AlertDescription>{notification}</AlertDescription>
          </Alert>
        ))}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList className="grid w-full grid-cols-6 bg-white rounded-lg shadow">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="activities">Activities</TabsTrigger>
            <TabsTrigger value="community">Community</TabsTrigger>
            <TabsTrigger value="rewards">Rewards</TabsTrigger>
            <TabsTrigger value="insights">Insights</TabsTrigger>
            <TabsTrigger value="challenges">Challenges</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <div className="grid grid-cols-2 gap-6">
              <Card className="col-span-2">
                <CardHeader>
                  <CardTitle>Welcome back, Eco Warrior!</CardTitle>
                  <CardDescription>Here's your environmental impact at a glance.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-4xl font-bold text-green-600">{data.ecoPoints}</p>
                      <p className="text-gray-500">Total Eco Points</p>
                    </div>
                    <div>
                      <p className="text-2xl font-bold">Rank #{data.communityRank}</p>
                      <p className="text-gray-500">in your community</p>
                    </div>
                    <div>
                      <Award size={48} className="text-yellow-400" />
                      <p className="text-gray-500">Top 10% Performer</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Carbon Footprint</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={data.carbonFootprint}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {data.carbonFootprint.map((entry, index) => (
                          <Cell key={cell-${index}} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Daily Activities</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={data.dailyActivities}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="points" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="activities">
            <Card>
              <CardHeader>
                <CardTitle>Log Your Eco-Friendly Activities</CardTitle>
                <CardDescription>Every action counts towards a greener future!</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { icon: Car, label: 'Transportation' },
                    { icon: Lightbulb, label: 'Energy Usage' },
                    { icon: ShoppingCart, label: 'Consumption' },
                    { icon: Trash, label: 'Waste Reduction' },
                    { icon: Recycle, label: 'Recycling' },
                    { icon: Leaf, label: 'Tree Planting' },
                  ].map(({ icon: Icon, label }) => (
                    <Button
                      key={label}
                      className="h-24 flex flex-col items-center justify-center"
                      variant="outline"
                      onClick={() => logActivity(label)}
                    >
                      <Icon size={24} />
                      <span className="mt-2">{label}</span>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="community">
            <div className="grid grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Community Impact Map</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-96 bg-gray-200 flex items-center justify-center">
                    <Map size={48} />
                    <p className="ml-2">Interactive community map would be displayed here</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Neighborhood Progress</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={data.monthlyProgress}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="carbonReduction" stroke="#8884d8" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="rewards">
            <Card>
              <CardHeader>
                <CardTitle>Redeem Eco Points</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { title: '10% Off', description: 'at local eco-store', points: 500 },
                    { title: 'Free Bus Pass', description: '1-week unlimited rides', points: 1000 },
                    { title: 'Tax Credit', description: '$50 off your next tax bill', points: 2000 },
                  ].map((reward, index) => (
                    <Card key={index}>
                      <CardHeader>
                        <CardTitle>{reward.title}</CardTitle>
                        <CardDescription>{reward.description}</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <p className="text-2xl font-bold text-green-600">{reward.points} points</p>
                      </CardContent>
                      <CardFooter>
                        <Button onClick={() => addNotification(${reward.title} redeemed!)}>Redeem</Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="insights">
            <Card>
              <CardHeader>
                <CardTitle>AI-Powered Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="mb-4">Based on your activity patterns, here are some personalized recommendations:</p>
                <ul className="list-disc pl-5 space-y-2">
                  <li>Switch to LED bulbs to reduce your energy consumption by up to 15%</li>
                  <li>Consider carpooling twice a week to cut your transportation emissions</li>
                  <li>Your neighborhood could reduce collective emissions by 5% through a community composting program</li>
                  <li>Installing a smart thermostat could save you 10% on heating and cooling costs</li>
                  <li>Participating in Meatless Mondays can reduce your weekly carbon footprint by 5%</li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="challenges">
            <div className="grid grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>30-Day Zero Waste Challenge</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Reduce your household waste to nearly zero for 30 days</p>
                  <Progress value={40} className="mt-4" />
                  <p className="text-sm text-gray-500 mt-2">40% complete</p>
                </CardContent>
                <CardFooter>
                  <Button onClick={() => addNotification('Logged progress for Zero Waste Challenge!')}>Log Progress</Button>
                </CardFooter>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Community Tree Planting</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Help plant 100 trees in your local area</p>
                  <Progress value={65} className="mt-4" />
                  <p className="text-sm text-gray-500 mt-2">65 trees planted</p>
                </CardContent>
                <CardFooter>
                  <Button onClick={() => addNotification('Logged new tree for Community Planting Challenge!')}>Log New Tree</Button>
                </CardFooter>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default EcoCitizenshipPlatform;
