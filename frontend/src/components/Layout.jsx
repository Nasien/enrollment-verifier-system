import { NavLink } from 'react-router-dom'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { useAuth } from '../context/AuthContext'

export default function Layout({ children }) {
  const { user, logout } = useAuth()

  return (
    <Container fluid>
      <Row>
        <Col md={3} lg={2} className="sidebar p-3">
          <div className="brand-box p-3 mb-4">
            <h5 className="mb-1">Enrollment Verifier</h5>
            <small>Scholarship Validation Portal</small>
          </div>
          <nav className="d-grid gap-2">
            <NavLink to="/">Dashboard</NavLink>
            <NavLink to="/upload">Upload Files</NavLink>
            <NavLink to="/sessions">Verification Sessions</NavLink>
          </nav>
          <div className="mt-4 pt-3 border-top border-light-subtle">
            <div className="small mb-2">Logged in as</div>
            <div className="fw-semibold">{user?.full_name}</div>
            <div className="small text-light">{user?.role}</div>
            <Button variant="light" size="sm" className="mt-3" onClick={logout}>Logout</Button>
          </div>
        </Col>
        <Col md={9} lg={10} className="p-4">
          {children}
        </Col>
      </Row>
    </Container>
  )
}
