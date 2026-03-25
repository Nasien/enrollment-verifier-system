import { useEffect, useState } from 'react'
import { Card, Col, Row, Table } from 'react-bootstrap'
import Layout from '../components/Layout'
import api from '../api/client'

export default function DashboardPage() {
  const [metrics, setMetrics] = useState(null)
  const [sessions, setSessions] = useState([])

  useEffect(() => {
    api.get('/dashboard/metrics').then((res) => setMetrics(res.data))
    api.get('/verification/sessions').then((res) => setSessions(res.data.slice(0, 5)))
  }, [])

  return (
    <Layout>
      <h2 className="page-title mb-4">Dashboard</h2>
      <Row className="g-3 mb-4">
        {[
          ['Total Uploads', metrics?.total_uploads || 0],
          ['Total Sessions', metrics?.total_sessions || 0],
          ['Exact Matches', metrics?.exact_matches || 0],
          ['Possible Matches', metrics?.possible_matches || 0],
        ].map(([title, value]) => (
          <Col md={6} xl={3} key={title}>
            <Card className="card-soft p-3">
              <div className="text-muted small">{title}</div>
              <div className="display-6 fw-bold">{value}</div>
            </Card>
          </Col>
        ))}
      </Row>

      <Card className="card-soft p-3">
        <h5 className="mb-3">Recent Verification Sessions</h5>
        <div className="table-responsive">
          <Table hover>
            <thead>
              <tr>
                <th>HEI</th>
                <th>AY</th>
                <th>Semester</th>
                <th>Scholarship</th>
                <th>Batch</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map((item) => (
                <tr key={item.id}>
                  <td>{item.hei_name}</td>
                  <td>{item.academic_year}</td>
                  <td>{item.semester}</td>
                  <td>{item.scholarship}</td>
                  <td>{item.batch}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Card>
    </Layout>
  )
}
