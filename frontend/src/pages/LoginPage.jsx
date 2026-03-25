import { useState } from 'react'
import { Alert, Button, Card, Col, Container, Form, Row } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState('')

  const handleSeed = async () => {
    await api.post('/auth/seed-admin')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setError('')
      await login(email, password)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={6} lg={4}>
          <Card className="card-soft p-4">
            <h3 className="mb-3">Sign in</h3>
            <p className="text-muted">Default admin account can be created with one click.</p>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control value={email} onChange={(e) => setEmail(e.target.value)} />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
              </Form.Group>
              <div className="d-grid gap-2">
                <Button type="submit">Login</Button>
                <Button variant="outline-secondary" type="button" onClick={handleSeed}>Seed Default Admin</Button>
              </div>
            </Form>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}
