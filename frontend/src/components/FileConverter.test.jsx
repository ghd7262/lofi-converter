import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import FileConverter from './FileConverter'

const mp3 = (name) => new File(['x'], name, { type: 'audio/mpeg' })

function mockApi() {
  const fetch = vi.fn(async (url) => {
    const body =
      url === '/jobs'
        ? {
            batch_id: 'b1',
            jobs: [{ job_id: 'j1', file_name: 'a.mp3' }],
            rejected: [{ file_name: 'b.mp3', error: { code: 'too_large', message: 'Max 20 MB' } }],
          }
        : { batch_id: 'b1', jobs: [{ job_id: 'j1', file_name: 'a.mp3', status: 'succeeded', error: null }] }
    return { ok: true, json: async () => body }
  })
  vi.stubGlobal('fetch', fetch)
  return fetch
}

test('dedupes files, converts checked ones, polls until done', async () => {
  const fetch = mockApi()
  const user = userEvent.setup()
  render(<FileConverter />)
  const input = screen.getByLabelText('Choose MP3 files')

  await user.upload(input, [mp3('a.mp3'), mp3('b.mp3'), mp3('c.mp3')])
  await user.upload(input, [mp3('a.mp3')])
  expect(screen.getAllByRole('checkbox')).toHaveLength(3)

  await user.click(screen.getByLabelText('c.mp3')) // uncheck c
  await user.click(screen.getByRole('button', { name: 'Convert to lo-fi' }))

  const sent = fetch.mock.calls[0][1].body.getAll('files').map((f) => f.name)
  expect(sent).toEqual(['a.mp3', 'b.mp3'])
  expect(screen.getByText('failed: Max 20 MB')).toBeInTheDocument()

  expect(await screen.findByRole('button', { name: 'Download a.mp3' }, { timeout: 3000 })).toBeInTheDocument()
  expect(fetch).toHaveBeenCalledWith('/batches/b1')
})
