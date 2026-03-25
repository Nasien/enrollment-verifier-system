import { useEffect, useState } from 'react'
import { Badge, Button, Card, Form, Modal, Table } from 'react-bootstrap'
import Layout from '../components/Layout'
import api from '../api/client'

export default function SessionsPage() {
  const [sessions, setSessions] = useState([])
  const [selected, setSelected] = useState(null)
  const [detail, setDetail] = useState(null)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    api.get('/verification/sessions').then((res) => setSessions(res.data))
  }, [])

  const openDetail = async (session) => {
    setSelected(session)
    const res = await api.get(`/verification/sessions/${session.id}`)
    setDetail(res.data)
  }

  const exportSession = async (sessionId) => {
    const response = await api.get(`/reports/session/${sessionId}/export`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `verification_${sessionId}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  }

  const filtered = sessions.filter((s) => [s.hei_name, s.academic_year, s.semester, s.batch || ''].join(' ').toLowerCase().includes(filter.toLowerCase()))

  return (
    <Layout>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="page-title mb-0">Verification Sessions</h2>
        <Form.Control style={{ maxWidth: 320 }} placeholder="Filter by HEI, AY, semester, batch" value={filter} onChange={(e) => setFilter(e.target.value)} />
      </div>
      <Card className="card-soft p-3">
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
                <th></th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((item) => (
                <tr key={item.id}>
                  <td>{item.hei_name}</td>
                  <td>{item.academic_year}</td>
                  <td>{item.semester}</td>
                  <td>{item.scholarship}</td>
                  <td>{item.batch}</td>
                  <td><Badge bg={item.status === 'completed' ? 'success' : 'secondary'}>{item.status}</Badge></td>
                  <td className="text-end">
                    <Button size="sm" className="me-2" onClick={() => openDetail(item)}>View</Button>
                    <Button size="sm" variant="outline-success" onClick={() => exportSession(item.id)}>Export</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Card>

      <Modal size="xl" show={!!selected} onHide={() => setSelected(null)}>
        <Modal.Header closeButton>
          <Modal.Title>Session Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {detail && (
            <>
              <div className="mb-3 d-flex gap-3 flex-wrap">
                <Badge bg="success">Exact: {detail.summary.exact_match}</Badge>
                <Badge bg="warning">Possible: {detail.summary.possible_match}</Badge>
                <Badge bg="danger">Not found: {detail.summary.not_found}</Badge>
                <Badge bg="primary">Total: {detail.summary.total}</Badge>
              </div>
              <div style={{ maxHeight: 500, overflow: 'auto' }}>
                <Table bordered hover size="sm">
                  <thead>
                    <tr>
                      <th>Grantee Name</th>
                      <th>Matched Name</th>
                      <th>Match Status</th>
                      <th>Score</th>
                      <th>Review Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detail.results.map((row) => (
                      <tr key={row.id}>
                        <td>{row.grantee_name}</td>
                        <td>{row.matched_name}</td>
                        <td>{row.match_status}</td>
                        <td>{row.match_score}</td>
                        <td>{row.review_status}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </>
          )}
        </Modal.Body>
      </Modal>
    </Layout>
  )
}
