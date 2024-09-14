async function D() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function F(e) {
  return await D(), e().then((t) => t.default);
}
function q(e) {
  const {
    gradio: t,
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...m) => {
        const b = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (c.length > 1) {
        let m = {
          ...s.props[c[0]] || {}
        };
        o[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const g = {
            ...s.props[c[a]] || {}
          };
          m[c[a]] = g, m = g;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, o;
      }
      const d = c[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function v() {
}
function L(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function M(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return v;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(e) {
  let t;
  return M(e, (i) => t = i)(), t;
}
const w = [];
function h(e, t = v) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if (L(e, u) && (e = u, i)) {
      const c = !w.length;
      for (const f of s)
        f[1](), w.push(f, e);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function n(u) {
    o(u(e));
  }
  function l(u, c = v) {
    const f = [u, c];
    return s.add(f), s.size === 1 && (i = t(o, n) || v), u(e), () => {
      s.delete(f), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: l
  };
}
const {
  getContext: j,
  setContext: N
} = window.__gradio__svelte__internal, Z = "$$ms-gr-antd-slots-key";
function B() {
  const e = h({});
  return N(Z, e);
}
const G = "$$ms-gr-antd-context-key";
function H(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = Q(), i = T({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    i.slotKey.set(c);
  }), J();
  const s = j(G), o = ((u = y(s)) == null ? void 0 : u.as_item) || e.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...e,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: f
    } = y(l);
    f && (c = c[f]), l.update((d) => ({
      ...d,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? y(s)[c.as_item] : y(s);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const V = "$$ms-gr-antd-slot-key";
function J() {
  N(V, h(void 0));
}
function Q() {
  return j(V);
}
const R = "$$ms-gr-antd-component-slot-context-key";
function T({
  slot: e,
  index: t,
  subIndex: i
}) {
  return N(R, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(i)
  });
}
function Ke() {
  return j(R);
}
function W(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var U = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (n = o(n, s(u)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return i.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var u in n)
        t.call(n, u) && n[u] && (l = o(l, u));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(U);
var $ = U.exports;
const x = /* @__PURE__ */ W($), {
  SvelteComponent: ee,
  assign: te,
  component_subscribe: P,
  create_component: ne,
  create_slot: se,
  destroy_component: ie,
  detach: oe,
  empty: le,
  flush: p,
  get_all_dirty_from_scope: re,
  get_slot_changes: ce,
  get_spread_object: A,
  get_spread_update: ae,
  handle_promise: ue,
  init: fe,
  insert: _e,
  mount_component: me,
  noop: _,
  safe_not_equal: de,
  transition_in: z,
  transition_out: I,
  update_await_block_branch: be,
  update_slot_base: pe
} = window.__gradio__svelte__internal;
function ge(e) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function he(e) {
  let t, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: x(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-notification"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[1].elem_id
      )
    },
    /*$mergedProps*/
    e[1].props,
    q(
      /*$mergedProps*/
      e[1]
    ),
    {
      message: (
        /*$mergedProps*/
        e[1].props.message || /*$mergedProps*/
        e[1].message
      )
    },
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      visible: (
        /*$mergedProps*/
        e[1].visible
      )
    },
    {
      onVisible: (
        /*func*/
        e[17]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [ye]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = te(o, s[n]);
  return t = new /*Notification*/
  e[20]({
    props: o
  }), {
    c() {
      ne(t.$$.fragment);
    },
    m(n, l) {
      me(t, n, l), i = !0;
    },
    p(n, l) {
      const u = l & /*$mergedProps, $slots, visible*/
      7 ? ae(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: x(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-notification"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && A(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && A(q(
        /*$mergedProps*/
        n[1]
      )), l & /*$mergedProps*/
      2 && {
        message: (
          /*$mergedProps*/
          n[1].props.message || /*$mergedProps*/
          n[1].message
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, l & /*$mergedProps*/
      2 && {
        visible: (
          /*$mergedProps*/
          n[1].visible
        )
      }, l & /*visible*/
      1 && {
        onVisible: (
          /*func*/
          n[17]
        )
      }]) : {};
      l & /*$$scope*/
      262144 && (u.$$scope = {
        dirty: l,
        ctx: n
      }), t.$set(u);
    },
    i(n) {
      i || (z(t.$$.fragment, n), i = !0);
    },
    o(n) {
      I(t.$$.fragment, n), i = !1;
    },
    d(n) {
      ie(t, n);
    }
  };
}
function ye(e) {
  let t;
  const i = (
    /*#slots*/
    e[16].default
  ), s = se(
    i,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, n) {
      s && s.m(o, n), t = !0;
    },
    p(o, n) {
      s && s.p && (!t || n & /*$$scope*/
      262144) && pe(
        s,
        i,
        o,
        /*$$scope*/
        o[18],
        t ? ce(
          i,
          /*$$scope*/
          o[18],
          n,
          null
        ) : re(
          /*$$scope*/
          o[18]
        ),
        null
      );
    },
    i(o) {
      t || (z(s, o), t = !0);
    },
    o(o) {
      I(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function we(e) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function Ce(e) {
  let t, i, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: we,
    then: he,
    catch: ge,
    value: 20,
    blocks: [, , ,]
  };
  return ue(
    /*AwaitedNotification*/
    e[3],
    s
  ), {
    c() {
      t = le(), s.block.c();
    },
    m(o, n) {
      _e(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, i = !0;
    },
    p(o, [n]) {
      e = o, be(s, e, n);
    },
    i(o) {
      i || (z(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        I(l);
      }
      i = !1;
    },
    d(o) {
      o && oe(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function ke(e, t, i) {
  let s, o, n, {
    $$slots: l = {},
    $$scope: u
  } = t;
  const c = F(() => import("./notification-D8tPBN4i.js"));
  let {
    gradio: f
  } = t, {
    props: d = {}
  } = t;
  const m = h(d);
  P(e, m, (r) => i(15, s = r));
  let {
    _internal: b = {}
  } = t, {
    message: a = ""
  } = t, {
    as_item: g
  } = t, {
    visible: C = !1
  } = t, {
    elem_id: k = ""
  } = t, {
    elem_classes: K = []
  } = t, {
    elem_style: S = {}
  } = t;
  const [E, X] = H({
    gradio: f,
    props: s,
    _internal: b,
    message: a,
    visible: C,
    elem_id: k,
    elem_classes: K,
    elem_style: S,
    as_item: g
  });
  P(e, E, (r) => i(1, o = r));
  const O = B();
  P(e, O, (r) => i(2, n = r));
  const Y = (r) => {
    i(0, C = r);
  };
  return e.$$set = (r) => {
    "gradio" in r && i(7, f = r.gradio), "props" in r && i(8, d = r.props), "_internal" in r && i(9, b = r._internal), "message" in r && i(10, a = r.message), "as_item" in r && i(11, g = r.as_item), "visible" in r && i(0, C = r.visible), "elem_id" in r && i(12, k = r.elem_id), "elem_classes" in r && i(13, K = r.elem_classes), "elem_style" in r && i(14, S = r.elem_style), "$$scope" in r && i(18, u = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && m.update((r) => ({
      ...r,
      ...d
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, message, visible, elem_id, elem_classes, elem_style, as_item*/
    65153 && X({
      gradio: f,
      props: s,
      _internal: b,
      message: a,
      visible: C,
      elem_id: k,
      elem_classes: K,
      elem_style: S,
      as_item: g
    });
  }, [C, o, n, c, m, E, O, f, d, b, a, g, k, K, S, s, l, Y, u];
}
class Se extends ee {
  constructor(t) {
    super(), fe(this, t, ke, Ce, de, {
      gradio: 7,
      props: 8,
      _internal: 9,
      message: 10,
      as_item: 11,
      visible: 0,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), p();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), p();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), p();
  }
  get message() {
    return this.$$.ctx[10];
  }
  set message(t) {
    this.$$set({
      message: t
    }), p();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), p();
  }
  get visible() {
    return this.$$.ctx[0];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), p();
  }
}
export {
  Se as I,
  Ke as g,
  h as w
};
